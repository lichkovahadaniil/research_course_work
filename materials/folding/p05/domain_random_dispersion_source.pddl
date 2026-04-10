;; A rotation (fold) at node n consists of one action rotate and two
;; folllowing passes over to remaining part of string starting at n.
;; In the first pass, all directions are corrected according to the
;; rotation applied, and all (at this point incorrect) (at ...) facts are
;; deleted. In the second pass, the correct (at ...) facts are set.
;; The reason we use two passes instead of one is to avoid the intersection
;; of the string with itself in the part that is currently moving. Consider
;; the following string:
;;        2-3
;;        | |
;;        1 4
;; and suppose we want to rotate 1 counterclockwise which results in the
;; following configuration:
;;      3-4
;;      |
;;      2-1
;; Now, note that 2 in the initial and 4 in the final configuration occupy
;; the same point in the plane. So, with one pass, we could end up with two
;; nodes occupying the same point, which we avoid by taking two passes instead
;; of one.
;;
(define (domain folding)
(:requirements :adl :action-costs)

(:types
    node - object
    coord - object
    direction - object
    rotation - object
)

(:constants
    left right up down - direction
    clockwise counterclockwise - rotation
)

(:predicates
    ;; ?dfrom rotated by ?r ends up as ?d2to
    (NEXT-DIRECTION ?dfrom - direction ?r - rotation ?d2to - direction)
    ;; ?cnext = ?c + 1
    (COORD-INC ?c ?cnext - coord)
    ;; Last node of the string
    (END-NODE ?n - node)
    ;; ?n2 follows right after ?n1 in the string
    (CONNECTED ?n1 ?n2 - node)

    ;; Position of the node in the grid
    (at ?n - node ?x ?y - coord)
    ;; Heading of the outgoing edge of this node
    (heading ?n - node ?dir - direction)
    ;; The coordinates are not occupied by any node
    (free ?x ?y - coord)
    ;; Flag indicating we are in the process of rotating the string
    (rotating)
    ;; Cursor storing that ?nstart was rotated by ?r and the next node to
    ;; process is ?n
    (node-first-pass-next ?nstart - node ?r - rotation ?n - node)
    ;; Cursor for the second pass
    (node-second-pass-next ?n - node)
)

(:functions
    (total-cost) - number
    (rotate-cost) - number
    (update-cost) - number
)


;; Rotates the string after this node and start the first pass computing
;; absolute directions and coordinates of other nodes)
