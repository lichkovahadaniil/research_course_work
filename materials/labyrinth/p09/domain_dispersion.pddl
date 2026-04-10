(define (domain labyrinth)
(:requirements :adl :action-costs)

(:types
    ;; card with 2 to 4 paths
    card - object
    direction - object
    ;; vertical direction: N S
    directionV - direction
    ;; horizontal directions: W E
    directionH - direction
    ;; values for positions of the card in the grid
    gridpos - object
)

(:constants
    S N - directionV
    W E - directionH
)

(:predicates
    ;; ordering of values for grid positions ?p1 = ?p2 + 1
    (NEXT ?p1 - gridpos ?p2 - gridpos)
    ;; maximal grid index
    (MAX-POS ?p - gridpos)
    ;; minimal grid index
    (MIN-POS ?p - gridpos)
    ;; moving from ?c in direction ?d is blocked by a wall
    (BLOCKED ?c - card ?d - direction)
    ;; robot is located on card ?c
    (robot-at ?c - card)
    ;; card ?c is positioned in the grid at ?x ?y
    (card-at ?c - card ?x - gridpos ?y - gridpos)
    ;; flag indicating that the robot left the maze e.i. that the goal has been reached
    (left)

    ;; flag to indicate that a card is currently moving an the robot cannot move
    (cards-moving)
    ;; flags to indicate that a row/column is rotating in the corresponding direction
    (cards-moving-west)
    (cards-moving-east)
    (cards-moving-south)
    (cards-moving-north)
    ;; the card whose position needs to be updated next while rotating
    (next-moving-card ?c - card)
    ;; the card that was removed to rotate and which needs to be placed at the beginning/end of the row/column
    (new-headtail-card ?c - card)

)

(:functions
    (total-cost) - number
    (move-robot-cost) - number
    (move-card) - number
)

;; moves the robot between to cards)

