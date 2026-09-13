#include "optgen.h"

OPTgen::OPTgen(std::size_t num_sets, std::size_t associativity, std::size_t history_multiplier) {
    this->num_sets = num_sets;
    this->associativity = associativity;
    this->history_cap = history_multiplier * associativity;
    sets.reserve(num_sets);
    for (std::size_t i = 0; i < num_sets; i++) {
        sets.push_back(set_state(history_cap));
    }
}

bool OPTgen::access(std::size_t set_idx, uint64_t address) {
    set_state& currSet = sets[set_idx];
    auto& occupancy = currSet.occupancy;
    auto& last = currSet.last;
    uint64_t current_time = currSet.curTime;
    bool hit = false;
    occupancy[current_time % history_cap] = 0;
    auto it = last.find(address);
    if (it != last.end()) {
        uint64_t start_time = it->second;
        uint64_t interval_length = current_time - start_time;
        if (interval_length < history_cap) {
            bool can_hit = true;
            for (uint64_t t = start_time; t < current_time; ++t) {
                if (occupancy[t % history_cap] >= associativity) {
                    can_hit = false;
                    break;
                }
            }
            if (can_hit) {
                hit = true;
                for (uint64_t t = start_time; t < current_time; ++t) {
                    occupancy[t % history_cap]++;
                }
            }
        }
    }
    last[address] = ++currSet.curTime;
    return hit;
}