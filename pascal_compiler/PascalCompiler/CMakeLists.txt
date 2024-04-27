cmake_minimum_required(VERSION 3.22)
project(PascalCompiler)

set(CMAKE_CXX_STANDARD 17)

set(antlr4-grammar-GENERATED_SRC
   ${PROJECT_SOURCE_DIR}/grammar/generated/PascalLexer.cpp 
   ${PROJECT_SOURCE_DIR}/grammar/generated/PascalParser.cpp
   ${PROJECT_SOURCE_DIR}/grammar/generated/PascalVisitor.cpp
   ${PROJECT_SOURCE_DIR}/grammar/generated/PascalBaseVisitor.cpp
)

#set(ANTLR_JAR_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/tools/antlr-4.13.1-complete.jar)

#find_package(ANTLR REQUIRED)
find_package(LLVM REQUIRED CONFIG)
find_package(Boost REQUIRED COMPONENTS system)

include_directories(/usr/include/antlr4-runtime ./parser)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/grammar/generated .)

link_libraries(antlr4-runtime LLVM)

add_custom_target(
    format
    ALL
    COMMAND /usr/bin/clang-format-15
    -style=LLVM
    -i
    ${ALL_SOURCE_FILES}
)

add_executable(${PROJECT_NAME}
    main.cpp
    visitor.cpp
    ${antlr4-grammar-GENERATED_SRC}
)

target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})
