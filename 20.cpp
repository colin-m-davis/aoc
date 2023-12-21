// AoC 2023, day 20

/*
flip-flop (%)
-------------
low or high, initially low
receives high -> ignored
receives low -> flips -> sends current state to all outs

conjunction (&)
---------------
remembers most recent pulse from each ins
initially remembers a low pulse from each one
when receives a pulse, updates memory for that input
if remembers ALL high pulses, sends low pulse
else sends a high pulse

broadcaster (unique)
--------------------
when receiving a pulse, sends that pulse to all outs
(button sends low pulse, so effectively sends low pulse to all outs)

button (implicit)
-----------------
sends low pulse to broadcaster

find
----
push the button 1000 times. return product of # high pulses and # low pulses
*/

#include "/Users/colindavis/.cmd/all.hpp"
#include <vector>
#include <utility>
#include <string>
#include <unordered_map>
#include <queue>
#include <tuple>
#include <fstream>
#include <memory>
#include <algorithm>

constexpr auto debug_light = false;
constexpr auto debug = false;

using Name = std::string;
using Pulse = bool;
constexpr Pulse low = false;
constexpr Pulse high = true;
Pulse flip(Pulse p) { return !p; }

struct Message {
    Name from;
    Name to;
    Pulse p;
};

class Module {
public:
    Name name;
    std::vector<Name> out_names;
    bool debug;
    virtual void receive(const Message& m) = 0;
    Module(const Name& name, const std::vector<Name>& out_names, bool debug = false)
        : name(name), out_names(out_names), debug(debug) {}
    void set_q(std::shared_ptr<std::queue<Message>> _q) { q = _q; }
protected:
    std::shared_ptr<std::queue<Message>> q;
    void send(Pulse p) {
        if (debug) cmd::print("  send");
        for (const auto& out_name : out_names) {
            if (debug) cmd::print("   ", out_name, p);
            q.get()->emplace(name, out_name, p);
        }
    }
};

class FlipFlop : public Module {
public:
    FlipFlop(const Name& name, const std::vector<Name>& out_names, bool debug = false)
        : Module(name, out_names, debug) {}
    Pulse current{low};
    virtual void receive(const Message& m) override {
        const auto& [from, to, p] = m;
        if (p == high) {
            if (debug) cmd::print("[flip-flop]", name, "not sending");
            return;
        }
        if (debug) cmd::print("[flip-flop]", name, "sending");
        current = flip(current);
        send(current);
    }
};

class Conjunction : public Module {
public:
    Conjunction(const Name& name, const std::vector<Name>& out_names, bool debug = false)
        : Module(name, out_names, debug) {}
    virtual void receive(const Message& m) override {
        const auto& [from, to, p] = m;
        last_pulses[from] = p;
        
        if (all_high()) {
            if (debug) cmd::print("[conjunction]", name, "sending (all high!)");
            send(low);
        } else {
            if (debug) cmd::print("[conjunction]", name, "sending (not all high)");
            send(high);
        }
    }
    void add_in(const std::string& in_name) {
        last_pulses[in_name] = low;
    }
    std::unordered_map<Name, Pulse> last_pulses;
private:
    auto all_high() -> bool {
        bool good = true;
        for (const auto& [in_name, last_pulse] : last_pulses) {
            if (last_pulse == low) {
                good = false;
                break;
            }
        }
        return good;
    }
};

class Broadcaster : public Module {
public:
    Broadcaster(const Name& name, const std::vector<Name>& out_names, bool debug = false)
        : Module(name, out_names, debug) {}
    virtual void receive(const Message& m) override {
        if (debug) cmd::print("[broadcaster]", name, "sending");
        send(low);
    }
};

auto parse_line(const std::string& line)
    -> std::tuple<std::string, Name, std::unique_ptr<Module>> {
    const auto parts = cmd::split(line, " -> ");
    const auto first_part = parts[0], second_part = parts[1];
    const auto out_names = cmd::split(second_part, ", ");

    std::unique_ptr<Module> module;
    std::vector<std::string> labels{"broadcaster", "%", "&"};
    for (const auto& label : labels) {
        if (first_part.starts_with(label)) {
            if (label == "broadcaster") {
                const std::string name = "broadcaster";
                return {label, name, std::make_unique<Broadcaster>(name, out_names, debug)};
            } else if (label == "%") {
                const auto name = first_part.substr(1);
                return {label, name, std::make_unique<FlipFlop>(name, out_names, debug)};
            } else if (label == "&") {
                const auto name = first_part.substr(1);
                return {label, name, std::make_unique<Conjunction>(name, out_names, debug)};
            } else {
                cmd::print("This shouldn't happen...");
            }
        }
    }
    cmd::print("This really shouldn't happen...");
    return {std::string{}, Name{}, std::make_unique<Conjunction>(Name{}, std::vector<Name>{})};
}

auto parse(const std::string& path) -> std::pair<
        std::shared_ptr<std::queue<Message>>,
        std::unordered_map<std::string, std::unique_ptr<Module>>> {
    std::ifstream f{path};
    const auto lines = cmd::readlines(f);

    auto q = std::make_shared<std::queue<Message>>();
    std::unordered_map<std::string, std::unique_ptr<Module>> m;
    std::vector<Name> conjunctions;
    for (const auto& line : lines) {
        auto [kind, name, module] = parse_line(line);
        module.get()->set_q(q);
        m[name] = std::move(module);
        if (kind == "&") conjunctions.push_back(name);
    }
    for (const auto& [name, module] : m) {
        for (const auto& out_name : module.get()->out_names) {
            const auto found = std::find(conjunctions.cbegin(), conjunctions.cend(), out_name);
            if (found != conjunctions.cend()) {
                const auto& conjunction_module = m[out_name].get();
                static_cast<Conjunction*>(conjunction_module)->add_in(name);
            }
        }
    }
    return {q, std::move(m)};
}

const int part = 2;
int main() {
    auto [q, m] = parse("input");
    if (part == 1) {
        const int N = 1000;
        auto total_count_low = 0;
        auto total_count_high = 0;
        for (auto i = 1; i <= N; ++i) {
            q.get()->emplace("button", "broadcaster", low);
            auto count_low = 0;
            auto count_high = 0;
            while (!(q.get()->empty())) {
                const auto message = q.get()->front();
                q.get()->pop();
                const auto& [from, to, p] = message;
                if (debug_light || debug)
                    cmd::print(from, std::string{"-"} + (p ? "high" : "low") + "->", to);

                if (p == low) ++count_low;
                else ++count_high;

                const auto found = m.find(to);
                if (found == m.cend()) {
                    if (debug) cmd::print("no module with name", to);
                } else {
                    const auto& mod = found->second;
                    mod.get()->receive(message);
                }
            }
            total_count_low += count_low;
            total_count_high += count_high;
            if (debug_light || debug)
                cmd::sep();
        }
        cmd::print("low:", total_count_low, "high:", total_count_high);
        cmd::print("product:", total_count_low * total_count_high);
    } else if (part == 2) {
        const Name target{"rx"};
        const Name prev{"kc"};
        const int inf = 1000000000;
        std::unordered_map<Name, int> needs;
        for (const auto& [in_name, _] : static_cast<Conjunction*>(m[prev].get())->last_pulses) {
            cmd::print(in_name, "...");
            needs[in_name] = inf;
        }
        bool complete = false;
        for (auto i = 1; !complete && i < inf; ++i) {
            q.get()->emplace("button", "broadcaster", low);
            auto count_low = 0;
            auto count_high = 0;
            while (!complete && !(q.get()->empty())) {
                const auto message = q.get()->front();
                q.get()->pop();
                const auto& [from, to, p] = message;
                if (debug_light || debug)
                    cmd::print(from, std::string{"-"} + (p ? "high" : "low") + "->", to);
                
                auto found_need = needs.find(from);
                if (found_need != needs.cend() && to == prev && p == high) {
                    if (found_need->second == inf) {
                        found_need->second = i;
                        bool all_done = true;
                        for (const auto& [need_name, iters] : needs) {
                            if (iters == inf) {
                                all_done = false;
                                break;
                            }
                        }
                        if (all_done) {
                            complete = true;
                            break;
                        }
                    }
                }

                const auto found = m.find(to);
                if (found == m.cend()) {
                    if (debug) cmd::print("no module with name", to);
                } else {
                    const auto& mod = found->second;
                    mod.get()->receive(message);
                }
            }
            if (debug_light || debug)
                cmd::sep();
        }
        long long ans = 1;
        for (const auto [need_name, iters] : needs) {
            ans *= iters;
        }
        cmd::print("Cycle lengths product bullshit:", ans);
    } else {
        cmd::print("There are only 2 parts to this problem!");
    }
    return 0;
}
