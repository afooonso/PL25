program ProdutoArray;

var
  numeros: array[1..5] of integer;
  i, produto: integer;

begin
  produto := 1;
  writeln('Introduza 5 números inteiros:');
  for i := 1 to 5 do
  begin
    readln(numeros[i]);
    produto := produto * numeros[i];
  end;
  writeln('O produto dos números é: ', produto);
end.
