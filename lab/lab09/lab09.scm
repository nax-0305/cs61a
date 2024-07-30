(define (over-or-under num1 num2) 
  (if (< num1 num2) 
      -1
      (if (= num1 num2) 
          0
          (if (> num1 num2)
              1)
    )
  )
)

; this is another way to solve this problem
; (define (over-or-under num1 num2) 
;   (cond ((< num1 num2) -1)
;         ((= num1 num2) 0)
;         ((> num1 num2) 1)
;   )
; )

(define (make-adder num) 
  (lambda (inc) (+ num inc))
)

(define (composed f g)
  (lambda (x) (f (g x)))
)

(define (repeat f n) 
  (lambda (x) 
    (if (= n 1)
        f(x)
        ; because the hint provided by cs61a
        ; also, the return of repeat is function, so it can be passed in composed function
        (composed f (repeat f (- n 1)))
    )
  )
)

(define (max a b)
  (if (> a b)
      a
      b))

(define (min a b)
  (if (> a b)
      b
      a))

(define (gcd a b) 
  (if (= b 0)
      a
      (gcd b (modulo a b))
  )
)

; using cons recusively, not for or while
(define (duplicate lst) 
  (if (null? lst)
      nil 
      (cons (car lst) (cons (car lst) (duplicate (cdr lst))))
  )
)

(expect (duplicate '(1 2 3)) (1 1 2 2 3 3))

(expect (duplicate '(1 1)) (1 1 1 1))

(define (deep-map fn s) 
  (if (null? s)
      nil
      if (list? (car s))
          cons((map fn (car s)) (deep-map fn cdr(s)))
          cons((fn (car s)) (deep-map fn cdr(s)))
  )
)