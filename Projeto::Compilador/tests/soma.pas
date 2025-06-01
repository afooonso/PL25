program BasicArithmetic;
var
  a, b, c: integer;
begin
  a := 3;
  b := 4;
  c := a + b * 2 - (a - b) div 2;
    writeln('Result of basic arithmetic operations: ', c);
end.

