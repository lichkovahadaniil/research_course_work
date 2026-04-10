(define (domain recharging-robots)
(:requirements :typing :adl :action-costs)
(:types
    location - object
    robot - object
    battery-level - object
    config - object
)

(:predicates
    ;; ?f1 is predecessor of ?f2 in the battery level, i.e., ?f2 = ?f1 + 1
    (BATTERY-PREDECESSOR ?f1 - battery-level ?f2 - battery-level)
    ;; Two locations are connected in the graph of locations
    (CONNECTED ?l1 - location ?l2 - location)
    ;; Definition of a guarding configuration, i.e., one atom per location
    ;; in each configuration
    (GUARD-CONFIG ?c - config ?l - location)
    ;; Robot is located at the given location
    (at ?r - robot ?l - location)
    ;; The remaining battery of the robot
    (battery ?r - robot ?f - battery-level)
    ;; Robot stopped and is guarding all locations connected to the
    ;; location where robot is located
    (stopped ?r - robot)
    ;; Location ?l is guarded by at least one robot
    (guarded ?l - location)
    ;; Configuration is fullfilled, i.e., all of its locations were guarded
    ;; at some point.
    (config-fullfilled ?c - config)
)

(:functions
    (move-cost) - number
    (recharge-cost) - number
    (total-cost) - number
)

;; Move the robot ?r from the location ?from to the location ?to while
;; consuming the battery -- it is decreased by one from ?fpre to ?fpost)
