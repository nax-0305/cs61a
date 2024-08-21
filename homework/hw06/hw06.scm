(define (square n) (* n n))

(define (pow base exp)
   (if (= exp 2) 
        (square base)
        (if (odd? exp) (* base (pow base (- exp 1)))
                (square (pow base (quotient exp 2)))
        )
   )
)


`(define (repeatedly-cube n x)
  (if (zero? n)
      x
      (let 
        ; even though only one binding, it is needful to use additional kuohao
        (
            (y (repeatedly-cube (- n 1) x))
        )
        (* y y y)))
)

(define (cddr s) (cdr (cdr s)))

(define (cadr s) (car (cdr s)))

(define (caddr s) (car (cddr s)))

(define (ascending? s) 
    (if (or (null? s) (null? (cdr s))) #t 
        (and (<= (car s) (cadr s)) (ascending? (cdr s)))
    )
)

(define (my-filter pred s) 
    (if (null? s) 
        nil
        (if (pred (car s))
            (cons (car s) (my-filter pred (cdr s)))
            (my-filter pred (cdr s))
        )
    )
)

(define (no-repeats s) 
    (if (null? s) 
        s
        (cons 
            (car s)
            ; produce rest list without (car s) every recursion
            (no-repeats (filter (lambda (x) (not (= (car s) x))) (cdr s)))
        )
    )
)

; helper function
; returns the values of lst that are bigger than x
; e.g., (larger-values 3 '(1 2 3 4 5 1 2 3 4 5)) --> (4 5 4 5)
(define (larger-values x lst)
  ______________________________________________)

(define (longest-increasing-subsequence lst)
  (if (null? lst)
      nil
      (begin (define first (car lst))
             (define rest (cdr lst))
             (define large-values-rest
                     (larger-values first rest))
             (define with-first
                     ______________________________________________)
             (define without-first
                     ______________________________________________)
             (if ______________________________________________
                 with-first
                 without-first))))
