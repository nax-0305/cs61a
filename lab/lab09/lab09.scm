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
  (define adder (lambda (x) (+ num x)))
  (adder x)
)

(define (composed f g) 'YOUR-CODE-HERE)

(define (repeat f n) 'YOUR-CODE-HERE)

(define (max a b)
  (if (> a b)
      a
      b))

(define (min a b)
  (if (> a b)
      b
      a))

(define (gcd a b) 'YOUR-CODE-HERE)

(define (duplicate lst) 'YOUR-CODE-HERE)

(expect (duplicate '(1 2 3)) (1 1 2 2 3 3))

(expect (duplicate '(1 1)) (1 1 1 1))

(define (deep-map fn s) 'YOUR-CODE-HERE)
