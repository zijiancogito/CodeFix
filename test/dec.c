#include <hexrays.h>
__int64 foo(signed int a1, signed int a2)
{
  while ( a1 != a2 )
  {
    if ( a1 <= a2 )
    {
      if ( a1 < a2 )
        a2 -= a1;
    }
    else
    {
      a1 -= a2;
    }
  }
  return (unsigned int)a1;
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  unsigned int v3; // eax
  unsigned int v5; // [rsp+18h] [rbp-8h]
  unsigned int v6; // [rsp+1Ch] [rbp-4h]

  if ( argc != 3 )
  {
    fprintf(stderr, "USAGE: %s <num1> <num2>\n", *argv);
    exit(1);
  }
  v5 = atoi(argv[1]);
  v6 = atoi(argv[2]);
  v3 = foo(v5, v6);
  printf("foo(%d, %d) = %d\n", v5, v6, v3);
  return 0;
}
