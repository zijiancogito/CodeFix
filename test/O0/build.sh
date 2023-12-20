#! /bin/sh
set -e

if [ $# -lt 2 ]; then
  echo "USAGE: $0 source binary"
  exit 1
fi

source="$1"
binary="$2"
shift 2


if grep -v include "$source" |
   gcc  -E -nostdinc -undef -O0 -I /idainclude/ -o - - |
   grep -qF "__asm" ;
then
  echo "Nice try."
  exit 1
fi

gcc "$@" -fno-asm -g -O0 -I /idainclude/ -o "$binary" "$source"
