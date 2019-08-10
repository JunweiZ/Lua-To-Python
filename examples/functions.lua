function bar(a, b, c)
  print(a, b, c)
  return (1 + 2)
end

v = bar(1, 2, 3)
print(v)

a = function (x, y) return x + y end
print(a(1, 2))

-- Closures and anonymous functions are ok:
function adder(x)
  -- The returned function is created when adder is
  -- called, and remembers the value of x:
  return function (y) return x + y end
end

v = adder(5)
print(v(2))
