(define (domain ricochet-robots)
(:requirements :typing :adl :action-costs)

(:types
    robot - object
    cell - object
    direction - object
)

(:predicates
    ;; ?cnext is right next to ?c in the direction of ?dir
    (NEXT ?c - cell ?cnext - cell ?dir - direction)
    ;; moving from ?c in the direction ?dir is blocked
    (BLOCKED ?c - cell ?dir - direction)
    ;; Robot ?r is located in the cell ?c
    (at ?r - robot ?c - cell)
    ;; No robot is located in the cell ?c
    (free ?c - cell)
    ;; No robot is moving anywhere
    (nothing-is-moving)
    ;; Robot ?r is moving in the direction ?dir
    (is-moving ?r - robot ?dir - direction)
)

(:functions
    (total-cost) - number

    ;; The costs of actions are configurable.
    ;; If we want to count only the number of movements of robots instead of
    ;; counting all steps from a cell to cell (as it would be in the real
    ;; game), then we need to set
    ;;      (= (go-cost) 1)
    ;;      (= (step-cost) 0)
    ;;      (= (stop-cost) 0)
    (go-cost) - number
    (step-cost) - number
    (stop-cost) - number
)

;; Starts movement of the robot ?r in the direction ?dir)
