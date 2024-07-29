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

; 使用cond来做更简洁一点
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
    (if (= n 0)
        1
        (* (f x) (repeat f (- n 1)))
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

(define (duplicate lst) 'YOUR-CODE-HERE)

(expect (duplicate '(1 2 3)) (1 1 2 2 3 3))

(expect (duplicate '(1 1)) (1 1 1 1))

(define (deep-map fn s) 'YOUR-CODE-HERE)