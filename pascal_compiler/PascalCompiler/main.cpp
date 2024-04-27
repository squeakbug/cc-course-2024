#include <iostream>

#include <boost/uuid/uuid.hpp>
#include <boost/uuid/uuid_generators.hpp>

#include "PascalBaseVisitor.h"
#include "PascalLexer.h"
#include "PascalParser.h"
#include "antlr4-runtime.h"

using namespace antlr4;

int main(int argc, const char *argv[]) {
  std::string filename = argv[1];
  std::ifstream stream;
  stream.open(filename);
  ANTLRInputStream input(stream);
  PascalLexer lexer(&input);
  CommonTokenStream tokens(&lexer);
  PascalParser parser(&tokens);

  return 0;
}