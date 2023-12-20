#include <stdio.h>
#include <stdlib.h>

long long foo(signed int a1, signed int a2)
{
  while ( a1 != a2 )
  {
    if ( a1 < a2 )
      a2 -= a1;
    else
      a1 -= a2;
  }
  return (unsigned int)a1;
}

int main(int argc, const char **argv)
{
  unsigned int v3;
  unsigned int v5;
  unsigned int v6;

  if ( argc != 3 )
  {
    fprintf(stderr, "USAGE: %s <num1> <num2>\n", *argv);
    exit(1);
  }
  v5 = atoi(argv[1]);
  v6 = atoi(argv[2]);
  v3 = foo(v5, v6);
  printf("foo(%d, %d) = %u\n", v5, v6, v3);
  return 0;
}