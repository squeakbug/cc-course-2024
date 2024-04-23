#pragma once

#include "PascalBaseVisitor.h"

class Visitor : public PascalBaseVisitor {
 public:
  explicit Visitor();

  antlrcpp::Any visitProgram(PascalParser::ProgramContext *ctx) override;
  antlrcpp::Any visitProgramHeading(PascalParser::ProgramHeadingContext *ctx) override;
  antlrcpp::Any visitIdentifier(PascalParser::IdentifierContext *ctx) override;
  antlrcpp::Any visitBlock(PascalParser::BlockContext *ctx) override;
  antlrcpp::Any visitUsesUnitsPart(PascalParser::UsesUnitsPartContext *ctx) override;
  antlrcpp::Any visitLabelDeclarationPart(PascalParser::LabelDeclarationPartContext *ctx) override;
  antlrcpp::Any visitLabel(PascalParser::LabelContext *ctx) override;
  antlrcpp::Any visitConstantDefinitionPart(PascalParser::ConstantDefinitionPartContext *ctx) override;
  antlrcpp::Any visitConstantDefinition(PascalParser::ConstantDefinitionContext *ctx) override;
  antlrcpp::Any visitConstantChr(PascalParser::ConstantChrContext *ctx) override;
  antlrcpp::Any visitConstant(PascalParser::ConstantContext *ctx) override;
  antlrcpp::Any visitUnsignedNumber(PascalParser::UnsignedNumberContext *ctx) override;
  antlrcpp::Any visitUnsignedInteger(PascalParser::UnsignedIntegerContext *ctx) override;
  antlrcpp::Any visitUnsignedReal(PascalParser::UnsignedRealContext *ctx) override;
  antlrcpp::Any visitSign(PascalParser::SignContext *ctx) override;
  antlrcpp::Any visitBool_(PascalParser::Bool_Context *ctx) override;
  antlrcpp::Any visitString(PascalParser::StringContext *ctx) override;
  antlrcpp::Any visitTypeDefinitionPart(PascalParser::TypeDefinitionPartContext *ctx) override;
  antlrcpp::Any visitTypeDefinition(PascalParser::TypeDefinitionContext *ctx) override;
  antlrcpp::Any visitFunctionType(PascalParser::FunctionTypeContext *ctx) override;
  antlrcpp::Any visitProcedureType(PascalParser::ProcedureTypeContext *ctx) override;
  antlrcpp::Any visitType_(PascalParser::Type_Context *ctx) override;
  antlrcpp::Any visitSimpleType(PascalParser::SimpleTypeContext *ctx) override;
  antlrcpp::Any visitScalarType(PascalParser::ScalarTypeContext *ctx) override;
  antlrcpp::Any visitSubrangeType(PascalParser::SubrangeTypeContext *ctx) override;
  antlrcpp::Any visitTypeIdentifier(PascalParser::TypeIdentifierContext *ctx) override;
  antlrcpp::Any visitStructuredType(PascalParser::StructuredTypeContext *ctx) override;
  antlrcpp::Any visitUnpackedStructuredType(PascalParser::UnpackedStructuredTypeContext *ctx) override;
  antlrcpp::Any visitStringtype(PascalParser::StringtypeContext *ctx) override;
  antlrcpp::Any visitArrayType(PascalParser::ArrayTypeContext *ctx) override;
  antlrcpp::Any visitTypeList(PascalParser::TypeListContext *ctx) override;
  antlrcpp::Any visitIndexType(PascalParser::IndexTypeContext *ctx) override;
  antlrcpp::Any visitComponentType(PascalParser::ComponentTypeContext *ctx) override;
  antlrcpp::Any visitRecordType(PascalParser::RecordTypeContext *ctx) override;
  antlrcpp::Any visitFieldList(PascalParser::FieldListContext *ctx) override;
  antlrcpp::Any visitFixedPart(PascalParser::FixedPartContext *ctx) override;
  antlrcpp::Any visitRecordSection(PascalParser::RecordSectionContext *ctx) override;
  antlrcpp::Any visitVariantPart(PascalParser::VariantPartContext *ctx) override;
  antlrcpp::Any visitTag(PascalParser::TagContext *ctx) override;
  antlrcpp::Any visitVariant(PascalParser::VariantContext *ctx) override;
  antlrcpp::Any visitSetType(PascalParser::SetTypeContext *ctx) override;
  antlrcpp::Any visitBaseType(PascalParser::BaseTypeContext *ctx) override;
  antlrcpp::Any visitFileType(PascalParser::FileTypeContext *ctx) override;
  antlrcpp::Any visitPointerType(PascalParser::PointerTypeContext *ctx) override;
  antlrcpp::Any visitVariableDeclarationPart(PascalParser::VariableDeclarationPartContext *ctx) override;
  antlrcpp::Any visitVariableDeclaration(PascalParser::VariableDeclarationContext *ctx) override;
  antlrcpp::Any visitProcedureAndFunctionDeclarationPart(PascalParser::ProcedureAndFunctionDeclarationPartContext *ctx) override;
  antlrcpp::Any visitProcedureOrFunctionDeclaration(PascalParser::ProcedureOrFunctionDeclarationContext *ctx) override;
  antlrcpp::Any visitProcedureDeclaration(PascalParser::ProcedureDeclarationContext *ctx) override;
  antlrcpp::Any visitFormalParameterList(PascalParser::FormalParameterListContext *ctx) override;
  antlrcpp::Any visitFormalParameterSection(PascalParser::FormalParameterSectionContext *ctx) override;
  antlrcpp::Any visitParameterGroup(PascalParser::ParameterGroupContext *ctx) override;
  antlrcpp::Any visitIdentifierList(PascalParser::IdentifierListContext *ctx) override;
  antlrcpp::Any visitConstList(PascalParser::ConstListContext *ctx) override;
  antlrcpp::Any visitFunctionDeclaration(PascalParser::FunctionDeclarationContext *ctx) override;
  antlrcpp::Any visitResultType(PascalParser::ResultTypeContext *ctx) override;
  antlrcpp::Any visitStatement(PascalParser::StatementContext *ctx) override;
  antlrcpp::Any visitUnlabelledStatement(PascalParser::UnlabelledStatementContext *ctx) override;
  antlrcpp::Any visitSimpleStatement(PascalParser::SimpleStatementContext *ctx) override;
  antlrcpp::Any visitAssignmentStatement(PascalParser::AssignmentStatementContext *ctx) override;
  antlrcpp::Any visitVariable(PascalParser::VariableContext *ctx) override;
  antlrcpp::Any visitExpression(PascalParser::ExpressionContext *ctx) override;
  antlrcpp::Any visitRelationaloperator(PascalParser::RelationaloperatorContext *ctx) override;
  antlrcpp::Any visitSimpleExpression(PascalParser::SimpleExpressionContext *ctx) override;
  antlrcpp::Any visitAdditiveoperator(PascalParser::AdditiveoperatorContext *ctx) override;
  antlrcpp::Any visitTerm(PascalParser::TermContext *ctx) override;
  antlrcpp::Any visitMultiplicativeoperator(PascalParser::MultiplicativeoperatorContext *ctx) override;
  antlrcpp::Any visitSignedFactor(PascalParser::SignedFactorContext *ctx) override;
  antlrcpp::Any visitFactor(PascalParser::FactorContext *ctx) override;
  antlrcpp::Any visitUnsignedConstant(PascalParser::UnsignedConstantContext *ctx) override;
  antlrcpp::Any visitFunctionDesignator(PascalParser::FunctionDesignatorContext *ctx) override;
  antlrcpp::Any visitParameterList(PascalParser::ParameterListContext *ctx) override;
  antlrcpp::Any visitSet_(PascalParser::Set_Context *ctx) override;
  antlrcpp::Any visitElementList(PascalParser::ElementListContext *ctx) override;
  antlrcpp::Any visitElement(PascalParser::ElementContext *ctx) override;
  antlrcpp::Any visitProcedureStatement(PascalParser::ProcedureStatementContext *ctx) override;
  antlrcpp::Any visitActualParameter(PascalParser::ActualParameterContext *ctx) override;
  antlrcpp::Any visitParameterwidth(PascalParser::ParameterwidthContext *ctx) override;
  antlrcpp::Any visitGotoStatement(PascalParser::GotoStatementContext *ctx) override;
  antlrcpp::Any visitEmptyStatement_(PascalParser::EmptyStatement_Context *ctx) override;
  antlrcpp::Any visitEmpty_(PascalParser::Empty_Context *ctx) override;
  antlrcpp::Any visitStructuredStatement(PascalParser::StructuredStatementContext *ctx) override;
  antlrcpp::Any visitCompoundStatement(PascalParser::CompoundStatementContext *ctx) override; ;
  antlrcpp::Any visitStatements(PascalParser::StatementsContext *ctx) override;
  antlrcpp::Any visitConditionalStatement(PascalParser::ConditionalStatementContext *ctx) override;
  antlrcpp::Any visitIfStatement(PascalParser::IfStatementContext *ctx) override;
  antlrcpp::Any visitCaseStatement(PascalParser::CaseStatementContext *ctx) override;
  antlrcpp::Any visitCaseListElement(PascalParser::CaseListElementContext *ctx) override;
  antlrcpp::Any visitRepetetiveStatement(PascalParser::RepetetiveStatementContext *ctx) override;
  antlrcpp::Any visitWhileStatement(PascalParser::WhileStatementContext *ctx) override;
  antlrcpp::Any visitRepeatStatement(PascalParser::RepeatStatementContext *ctx) override;
  antlrcpp::Any visitForStatement(PascalParser::ForStatementContext *ctx) override;
  antlrcpp::Any visitForList(PascalParser::ForListContext *ctx) override;
  antlrcpp::Any visitInitialValue(PascalParser::InitialValueContext *ctx) override;
  antlrcpp::Any visitFinalValue(PascalParser::FinalValueContext *ctx) override;
  antlrcpp::Any visitWithStatement(PascalParser::WithStatementContext *ctx) override;
  antlrcpp::Any visitRecordVariableList(PascalParser::RecordVariableListContext *ctx) override;

 private:
  
};