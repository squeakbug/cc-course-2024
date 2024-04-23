using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Antlr4;
using Antlr4.Runtime;
using Antlr4.Runtime.Misc;
using Antlr4.Runtime.Tree;
using LLVMSharp;

using SimpleCompiler;
using SimpleCompiler.Content;


LLVMModuleRef module = LLVM.ModuleCreateWithName("my cool jit");
LLVMBuilderRef builder = LLVM.CreateBuilder();

LLVM.LinkInMCJIT();
LLVM.InitializeX86TargetInfo();
LLVM.InitializeX86Target();
LLVM.InitializeX86TargetMC();
if (LLVM.CreateExecutionEngineForModule(out var engine, module, out var errorMessage).Value == 1)
{
    Console.WriteLine(errorMessage);
    return;
}
LLVMPassManagerRef passManager = LLVM.CreateFunctionPassManagerForModule(module);
LLVM.AddBasicAliasAnalysisPass(passManager);
LLVM.AddPromoteMemoryToRegisterPass(passManager);
LLVM.AddInstructionCombiningPass(passManager);
LLVM.AddReassociatePass(passManager);
LLVM.AddGVNPass(passManager);
LLVM.AddCFGSimplificationPass(passManager);
LLVM.InitializeFunctionPassManager(passManager);

var filename = @"Content/test.simple";
var fileContent = File.ReadAllText(filename);
var inputStream = new AntlrInputStream(fileContent);
var simpleLexer = new SimpleLexer(inputStream);
var commonTokenStream = new CommonTokenStream(simpleLexer);
var simpleParser = new SimpleParser(commonTokenStream);
var simpleContext = simpleParser.program();
var simpleVisitor = new SimpleVisitor(passManager, builder);

Console.WriteLine("Before visiting");

simpleVisitor.Visit(simpleContext);

Console.WriteLine("After visiting");

LLVM.VerifyModule(module, LLVMVerifierFailureAction.LLVMPrintMessageAction, out string str);
LLVM.DumpModule(module);
LLVM.WriteBitcodeToFile(module, "compiled.bc");
LLVM.PrintModuleToFile(module, "compiled.ll", out string errorMsg);
LLVM.DisposePassManager(passManager);
LLVM.DisposeModule(module);
