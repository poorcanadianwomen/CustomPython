/* CustomPython Autocompiler
 * Python -> x86-64 ASM transpiler for CustomPython OS
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/* Token types */
typedef enum {
    TOKEN_EOF,
    TOKEN_NEWLINE,
    TOKEN_INDENT,
    TOKEN_DEDENT,
    TOKEN_NAME,
    TOKEN_NUMBER,
    TOKEN_STRING,
    TOKEN_PLUS,
    TOKEN_MINUS,
    TOKEN_STAR,
    TOKEN_SLASH,
    TOKEN_DOUBLE_SLASH,
    TOKEN_PERCENT,
    TOKEN_POWER,
    TOKEN_EQUALS,
    TOKEN_PLUSEQ,
    TOKEN_MINUSEQ,
    TOKEN_STAREQ,
    TOKEN_SLASHEQ,
    TOKEN_PERCENTEQ,
    TOKEN_POWEREQ,
    TOKEN_EQEQ,
    TOKEN_NOTEQ,
    TOKEN_LESSTHAN,
    TOKEN_LESSEQ,
    TOKEN_GREATERTHAN,
    TOKEN_GREATEREQ,
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_LBRACKET,
    TOKEN_RBRACKET,
    TOKEN_LBRACE,
    TOKEN_RBRACE,
    TOKEN_COMMA,
    TOKEN_COLON,
    TOKEN_DOT,
    TOKEN_SEMICOLON,
    TOKEN_AND,
    TOKEN_OR,
    TOKEN_NOT,
    TOKEN_TRUE,
    TOKEN_FALSE,
    TOKEN_NONE,
    TOKEN_IF,
    TOKEN_ELIF,
    TOKEN_ELSE,
    TOKEN_WHILE,
    TOKEN_FOR,
    TOKEN_BREAK,
    TOKEN_CONTINUE,
    TOKEN_DEF,
    TOKEN_RETURN,
    TOKEN_CLASS,
    TOKEN_IMPORT,
    TOKEN_FROM,
    TOKEN_AS,
    TOKEN_PASS,
    TOKEN_RAISE,
    TOKEN_TRY,
    TOKEN_EXCEPT,
    TOKEN_FINALLY,
    TOKEN_WITH,
    TOKEN_YIELD,
    TOKEN_LAMBDA,
    TOKEN_GLOBAL,
    TOKEN_NONLOCAL,
    TOKEN_ASSERT,
    TOKEN_DEL,
    TOKEN_IN,
    TOKEN_IS,
} TokenType;

/* Token structure */
typedef struct {
    TokenType type;
    char *value;
    int line;
    int col;
} Token;

/* Lexer */
typedef struct {
    const char *source;
    int pos;
    int line;
    int col;
    Token current;
    Token next;
} Lexer;

/* AST node types */
typedef enum {
    NODE_PROGRAM,
    NODE_FUNCTION_DEF,
    NODE_CLASS_DEF,
    NODE_ASSIGN,
    NODE_IF,
    NODE_WHILE,
    NODE_FOR,
    NODE_RETURN,
    NODE_CALL,
    NODE_BINARY_OP,
    NODE_UNARY_OP,
    NODE_NUMBER,
    NODE_STRING,
    NODE_NAME,
    NODE_LIST,
    NODE_DICT,
    NODE_NONE,
    NODE_TRUE,
    NODE_FALSE,
    NODE_PASS,
    NODE_BREAK,
    NODE_CONTINUE,
} NodeType;

/* AST node */
typedef struct ASTNode {
    NodeType type;
    union {
        struct { struct ASTNode **stmts; int count; } program;
        struct { char *name; struct ASTNode *body; struct ASTNode **args; int arg_count; } function_def;
        struct { char *name; struct ASTNode *body; } class_def;
        struct { char *name; struct ASTNode *value; } assign;
        struct { struct ASTNode *cond; struct ASTNode *body; struct ASTNode *else_body; } if_stmt;
        struct { struct ASTNode *cond; struct ASTNode *body; } while_stmt;
        struct { char *var; struct ASTNode *iter; struct ASTNode *body; } for_stmt;
        struct { struct ASTNode *value; } return_stmt;
        struct { char *func; struct ASTNode **args; int arg_count; } call;
        struct { char *op; struct ASTNode *left; struct ASTNode *right; } binary_op;
        struct { char *op; struct ASTNode *operand; } unary_op;
        struct { long value; } number;
        struct { char *value; } string;
        struct { char *name; } name;
    } data;
} ASTNode;

/* Code generator */
typedef struct {
    FILE *output;
    int label_count;
    int stack_offset;
    int locals_count;
    char *locals[256];
} CodeGen;

/* Initialize lexer */
void lexer_init(Lexer *lex, const char *source) {
    lex->source = source;
    lex->pos = 0;
    lex->line = 1;
    lex->col = 1;
    lex->current.type = TOKEN_EOF;
    lex->current.value = NULL;
    lex->next.type = TOKEN_EOF;
    lex->next.value = NULL;
}

/* Get next token */
void lexer_next_token(Lexer *lex) {
    /* Skip whitespace */
    while (lex->source[lex->pos] == ' ' || lex->source[lex->pos] == '\t') {
        lex->col++;
        lex->pos++;
    }
    
    /* Handle end of input */
    if (lex->source[lex->pos] == '\0') {
        lex->next.type = TOKEN_EOF;
        lex->next.value = NULL;
        return;
    }
    
    /* Handle newlines */
    if (lex->source[lex->pos] == '\n') {
        lex->next.type = TOKEN_NEWLINE;
        lex->line++;
        lex->col = 1;
        lex->pos++;
        return;
    }
    
    /* Handle comments */
    if (lex->source[lex->pos] == '#') {
        while (lex->source[lex->pos] != '\n' && lex->source[lex->pos] != '\0') {
            lex->pos++;
        }
        lexer_next_token(lex);
        return;
    }
    
    /* Handle numbers */
    if (isdigit(lex->source[lex->pos])) {
        int start = lex->pos;
        while (isdigit(lex->source[lex->pos]) || lex->source[lex->pos] == '.') {
            lex->pos++;
        }
        lex->next.type = TOKEN_NUMBER;
        lex->next.value = strndup(lex->source + start, lex->pos - start);
        lex->col += lex->pos - start;
        return;
    }
    
    /* Handle strings */
    if (lex->source[lex->pos] == '"' || lex->source[lex->pos] == '\'') {
        char quote = lex->source[lex->pos];
        lex->pos++;
        int start = lex->pos;
        while (lex->source[lex->pos] != quote && lex->source[lex->pos] != '\0') {
            lex->pos++;
        }
        lex->next.type = TOKEN_STRING;
        lex->next.value = strndup(lex->source + start, lex->pos - start);
        lex->col += lex->pos - start + 2;
        lex->pos++;  /* Skip closing quote */
        return;
    }
    
    /* Handle names and keywords */
    if (isalpha(lex->source[lex->pos]) || lex->source[lex->pos] == '_') {
        int start = lex->pos;
        while (isalnum(lex->source[lex->pos]) || lex->source[lex->pos] == '_') {
            lex->pos++;
        }
        lex->next.value = strndup(lex->source + start, lex->pos - start);
        lex->col += lex->pos - start;
        
        /* Check for keywords */
        if (strcmp(lex->next.value, "if") == 0) lex->next.type = TOKEN_IF;
        elif (strcmp(lex->next.value, "elif") == 0) lex->next.type = TOKEN_ELIF;
        elif (strcmp(lex->next.value, "else") == 0) lex->next.type = TOKEN_ELSE;
        elif (strcmp(lex->next.value, "while") == 0) lex->next.type = TOKEN_WHILE;
        elif (strcmp(lex->next.value, "for") == 0) lex->next.type = TOKEN_FOR;
        elif (strcmp(lex->next.value, "def") == 0) lex->next.type = TOKEN_DEF;
        elif (strcmp(lex->next.value, "return") == 0) lex->next.type = TOKEN_RETURN;
        elif (strcmp(lex->next.value, "class") == 0) lex->next.type = TOKEN_CLASS;
        elif (strcmp(lex->next.value, "import") == 0) lex->next.type = TOKEN_IMPORT;
        elif (strcmp(lex->next.value, "from") == 0) lex->next.type = TOKEN_FROM;
        elif (strcmp(lex->next.value, "True") == 0) lex->next.type = TOKEN_TRUE;
        elif (strcmp(lex->next.value, "False") == 0) lex->next.type = TOKEN_FALSE;
        elif (strcmp(lex->next.value, "None") == 0) lex->next.type = TOKEN_NONE;
        elif (strcmp(lex->next.value, "and") == 0) lex->next.type = TOKEN_AND;
        elif (strcmp(lex->next.value, "or") == 0) lex->next.type = TOKEN_OR;
        elif (strcmp(lex->next.value, "not") == 0) lex->next.type = TOKEN_NOT;
        elif (strcmp(lex->next.value, "pass") == 0) lex->next.type = TOKEN_PASS;
        elif (strcmp(lex->next.value, "break") == 0) lex->next.type = TOKEN_BREAK;
        elif (strcmp(lex->next.value, "continue") == 0) lex->next.type = TOKEN_CONTINUE;
        elif (strcmp(lex->next.value, "lambda") == 0) lex->next.type = TOKEN_LAMBDA;
        elif (strcmp(lex->next.value, "global") == 0) lex->next.type = TOKEN_GLOBAL;
        elif (strcmp(lex->next.value, "nonlocal") == 0) lex->next.type = TOKEN_NONLOCAL;
        elif (strcmp(lex->next.value, "assert") == 0) lex->next.type = TOKEN_ASSERT;
        elif (strcmp(lex->next.value, "del") == 0) lex->next.type = TOKEN_DEL;
        elif (strcmp(lex->next.value, "in") == 0) lex->next.type = TOKEN_IN;
        elif (strcmp(lex->next.value, "is") == 0) lex->next.type = TOKEN_IS;
        else lex->next.type = TOKEN_NAME;
        
        return;
    }
    
    /* Handle operators */
    switch (lex->source[lex->pos]) {
        case '+':
            lex->pos++;
            if (lex->source[lex->pos] == '=') {
                lex->next.type = TOKEN_PLUSEQ;
                lex->pos++;
            } else {
                lex->next.type = TOKEN_PLUS;
            }
            break;
        case '-':
            lex->pos++;
            if (lex->source[lex->pos] == '=') {
                lex->next.type = TOKEN_MINUSEQ;
                lex->pos++;
            } else {
                lex->next.type = TOKEN_MINUS;
            }
            break;
        case '*':
            lex->pos++;
            if (lex->source[lex->pos] == '*') {
                lex->pos++;
                if (lex->source[lex->pos] == '=') {
                    lex->next.type = TOKEN_POWEREQ;
                    lex->pos++;
                } else {
                    lex->next.type = TOKEN_POWER;
                }
            } elif (lex->source[lex->pos] == '=') {
                lex->next.type = TOKEN_STAREQ;
                lex->pos++;
            } else {
                lex->next.type = TOKEN_STAR;
            }
            break;
        case '/':
            lex->pos++;
            if (lex->source[lex->pos] == '/') {
                lex->pos++;
                if (lex->source[lex->pos] == '=') {
                    lex->next.type = TOKEN_SLASHEQ;
                    lex->pos++;
                } else {
                    lex->next.type = TOKEN_DOUBLE_SLASH;
                }
            } elif (lex->source[lex->pos] == '=') {
                lex->next.type = TOKEN_SLASHEQ;
                lex->pos++;
            } else {
                lex->next.type = TOKEN_SLASH;
            }
            break;
        case '%':
            lex->pos++;
            if (lex->source[lex->pos] == '=') {
                lex->next.type = TOKEN_PERCENTEQ;
                lex->pos++;
            } else {
                lex->next.type = TOKEN_PERCENT;
            }
            break;
        case '=':
            lex->pos++;
            if (lex->source[lex->pos] == '=') {
                lex->next.type = TOKEN_EQEQ;
                lex->pos++;
            } else {
                lex->next.type = TOKEN_EQUALS;
            }
            break;
        case '!':
            lex->pos++;
            if (lex->source[lex->pos] == '=') {
                lex->next.type = TOKEN_NOTEQ;
                lex->pos++;
            } else {
                /* Error */
                lex->next.type = TOKEN_EOF;
            }
            break;
        case '<':
            lex->pos++;
            if (lex->source[lex->pos] == '=') {
                lex->next.type = TOKEN_LESSEQ;
                lex->pos++;
            } else {
                lex->next.type = TOKEN_LESSTHAN;
            }
            break;
        case '>':
            lex->pos++;
            if (lex->source[lex->pos] == '=') {
                lex->next.type = TOKEN_GREATEREQ;
                lex->pos++;
            } else {
                lex->next.type = TOKEN_GREATERTHAN;
            }
            break;
        case '(':
            lex->next.type = TOKEN_LPAREN;
            lex->pos++;
            break;
        case ')':
            lex->next.type = TOKEN_RPAREN;
            lex->pos++;
            break;
        case '[':
            lex->next.type = TOKEN_LBRACKET;
            lex->pos++;
            break;
        case ']':
            lex->next.type = TOKEN_RBRACKET;
            lex->pos++;
            break;
        case '{':
            lex->next.type = TOKEN_LBRACE;
            lex->pos++;
            break;
        case '}':
            lex->next.type = TOKEN_RBRACE;
            lex->pos++;
            break;
        case ',':
            lex->next.type = TOKEN_COMMA;
            lex->pos++;
            break;
        case ':':
            lex->next.type = TOKEN_COLON;
            lex->pos++;
            break;
        case '.':
            lex->next.type = TOKEN_DOT;
            lex->pos++;
            break;
        case ';':
            lex->next.type = TOKEN_SEMICOLON;
            lex->pos++;
            break;
        default:
            lex->pos++;
            lex->next.type = TOKEN_EOF;
            break;
    }
}

/* Advance to next token */
void lexer_advance(Lexer *lex) {
    if (lex->current.value) {
        free(lex->current.value);
    }
    lex->current = lex->next;
    lex->next.type = TOKEN_EOF;
    lex->next.value = NULL;
    lexer_next_token(lex);
}

/* Create AST node */
ASTNode *ast_node_create(NodeType type) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    if (node) {
        node->type = type;
    }
    return node;
}

/* Code generation: emit a line of assembly */
void codegen_emit(CodeGen *gen, const char *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    fprintf(gen->output, "    ");
    vfprintf(gen->output, fmt, args);
    fprintf(gen->output, "\n");
    va_end(args);
}

/* Code generation: emit a label */
void codegen_label(CodeGen *gen, const char *label) {
    fprintf(gen->output, "%s:\n", label);
}

/* Code generation: generate a unique label */
void codegen_unique_label(CodeGen *gen, char *buf, size_t len) {
    snprintf(buf, len, ".L%d", gen->label_count++);
}

/* Code generation: generate a number literal */
void codegen_number(CodeGen *gen, long value) {
    codegen_emit(gen, "mov rax, %ld", value);
}

/* Code generation: generate a string literal */
void codegen_string(CodeGen *gen, const char *str) {
    /* Create string in data section */
    char label[64];
    codegen_unique_label(gen, label, sizeof(label));
    
    fprintf(gen->output, ".section .rodata\n");
    codegen_label(gen, label);
    fprintf(gen->output, "    .string \"%s\"\n", label);
    fprintf(gen->output, ".section .text\n");
    
    codegen_emit(gen, "lea rax, [rip + %s]", label);
}

/* Code generation: generate an expression */
void codegen_expr(CodeGen *gen, ASTNode *node) {
    if (!node) return;
    
    switch (node->type) {
        case NODE_NUMBER:
            codegen_number(gen, node->data.number.value);
            break;
            
        case NODE_STRING:
            codegen_string(gen, node->data.string.value);
            break;
            
        case NODE_TRUE:
            codegen_number(gen, 1);
            break;
            
        case NODE_FALSE:
            codegen_number(gen, 0);
            break;
            
        case NODE_NONE:
            codegen_number(gen, 0);
            break;
            
        case NODE_NAME:
            /* Load variable from stack */
            codegen_emit(gen, "mov rax, [rbp - %d]", (int)(node->data.name.name[0] * 4));
            break;
            
        case NODE_BINARY_OP:
            codegen_expr(gen, node->data.binary_op.right);
            codegen_emit(gen, "push rax");
            codegen_expr(gen, node->data.binary_op.left);
            codegen_emit(gen, "pop rcx");
            
            if (strcmp(node->data.binary_op.op, "+") == 0) {
                codegen_emit(gen, "add rax, rcx");
            } elif (strcmp(node->data.binary_op.op, "-") == 0) {
                codegen_emit(gen, "sub rax, rcx");
            } elif (strcmp(node->data.binary_op.op, "*") == 0) {
                codegen_emit(gen, "imul rax, rcx");
            } elif (strcmp(node->data.binary_op.op, "/") == 0) {
                codegen_emit(gen, "cqo");
                codegen_emit(gen, "idiv rcx");
            } elif (strcmp(node->data.binary_op.op, "%") == 0) {
                codegen_emit(gen, "cqo");
                codegen_emit(gen, "idiv rcx");
                codegen_emit(gen, "mov rax, rdx");
            } elif (strcmp(node->data.binary_op.op, "==") == 0) {
                codegen_emit(gen, "cmp rax, rcx");
                codegen_emit(gen, "sete al");
                codegen_emit(gen, "movzx rax, al");
            } elif (strcmp(node->data.binary_op.op, "!=") == 0) {
                codegen_emit(gen, "cmp rax, rcx");
                codegen_emit(gen, "setne al");
                codegen_emit(gen, "movzx rax, al");
            } elif (strcmp(node->data.binary_op.op, "<") == 0) {
                codegen_emit(gen, "cmp rax, rcx");
                codegen_emit(gen, "setl al");
                codegen_emit(gen, "movzx rax, al");
            } elif (strcmp(node->data.binary_op.op, "<=") == 0) {
                codegen_emit(gen, "cmp rax, rcx");
                codegen_emit(gen, "setle al");
                codegen_emit(gen, "movzx rax, al");
            } elif (strcmp(node->data.binary_op.op, ">") == 0) {
                codegen_emit(gen, "cmp rax, rcx");
                codegen_emit(gen, "setg al");
                codegen_emit(gen, "movzx rax, al");
            } elif (strcmp(node->data.binary_op.op, ">=") == 0) {
                codegen_emit(gen, "cmp rax, rcx");
                codegen_emit(gen, "setge al");
                codegen_emit(gen, "movzx rax, al");
            } elif (strcmp(node->data.binary_op.op, "and") == 0) {
                codegen_emit(gen, "and rax, rcx");
            } elif (strcmp(node->data.binary_op.op, "or") == 0) {
                codegen_emit(gen, "or rax, rcx");
            }
            break;
            
        case NODE_UNARY_OP:
            codegen_expr(gen, node->data.unary_op.operand);
            if (strcmp(node->data.unary_op.op, "-") == 0) {
                codegen_emit(gen, "neg rax");
            } elif (strcmp(node->data.unary_op.op, "not") == 0) {
                codegen_emit(gen, "test rax, rax");
                codegen_emit(gen, "setz al");
                codegen_emit(gen, "movzx rax, al");
            }
            break;
            
        case NODE_CALL:
            /* Push arguments in reverse order */
            for (int i = node->data.call.arg_count - 1; i >= 0; i--) {
                codegen_expr(gen, node->data.call.args[i]);
                codegen_emit(gen, "push rax");
            }
            
            /* Call function */
            codegen_emit(gen, "call %s", node->data.call.func);
            
            /* Clean up arguments */
            if (node->data.call.arg_count > 0) {
                codegen_emit(gen, "add rsp, %d", node->data.call.arg_count * 8);
            }
            break;
            
        default:
            break;
    }
}

/* Code generation: generate a statement */
void codegen_stmt(CodeGen *gen, ASTNode *node) {
    if (!node) return;
    
    switch (node->type) {
        case NODE_ASSIGN:
            codegen_expr(gen, node->data.assign.value);
            codegen_emit(gen, "mov [rbp - %d], rax", (int)(node->data.assign.name[0] * 4));
            break;
            
        case NODE_IF:
            {
                char end_label[64], else_label[64];
                codegen_unique_label(gen, end_label, sizeof(end_label));
                codegen_unique_label(gen, else_label, sizeof(else_label));
                
                codegen_expr(gen, node->data.if_stmt.cond);
                codegen_emit(gen, "test rax, rax");
                codegen_emit(gen, "je %s", else_label);
                
                codegen_stmt(gen, node->data.if_stmt.body);
                
                if (node->data.if_stmt.else_body) {
                    char body_end[64];
                    codegen_unique_label(gen, body_end, sizeof(body_end));
                    codegen_emit(gen, "jmp %s", body_end);
                    codegen_label(gen, else_label);
                    codegen_stmt(gen, node->data.if_stmt.else_body);
                    codegen_label(gen, body_end);
                } else {
                    codegen_label(gen, else_label);
                }
            }
            break;
            
        case NODE_WHILE:
            {
                char start_label[64], end_label[64];
                codegen_unique_label(gen, start_label, sizeof(start_label));
                codegen_unique_label(gen, end_label, sizeof(end_label));
                
                codegen_label(gen, start_label);
                codegen_expr(gen, node->data.while_stmt.cond);
                codegen_emit(gen, "test rax, rax");
                codegen_emit(gen, "je %s", end_label);
                
                codegen_stmt(gen, node->data.while_stmt.body);
                codegen_emit(gen, "jmp %s", start_label);
                
                codegen_label(gen, end_label);
            }
            break;
            
        case NODE_RETURN:
            if (node->data.return_stmt.value) {
                codegen_expr(gen, node->data.return_stmt.value);
            } else {
                codegen_emit(gen, "xor eax, eax");
            }
            codegen_emit(gen, "mov rsp, rbp");
            codegen_emit(gen, "pop rbp");
            codegen_emit(gen, "ret");
            break;
            
        case NODE_PASS:
            /* Do nothing */
            break;
            
        case NODE_FUNCTION_DEF:
            {
                char func_label[64];
                snprintf(func_label, sizeof(func_label), "_%s", node->data.function_def.name);
                
                fprintf(gen->output, ".globl %s\n", func_label);
                fprintf(gen->output, ".type %s, @function\n", func_label);
                codegen_label(gen, func_label);
                
                /* Prologue */
                codegen_emit(gen, "push rbp");
                codegen_emit(gen, "mov rbp, rsp");
                
                /* Allocate space for locals */
                gen->stack_offset = 0;
                codegen_stmt(gen, node->data.function_def.body);
                
                /* Epilogue */
                codegen_emit(gen, "mov rsp, rbp");
                codegen_emit(gen, "pop rbp");
                codegen_emit(gen, "ret");
            }
            break;
            
        default:
            break;
    }
}

/* Code generation: generate the program */
void codegen_program(CodeGen *gen, ASTNode *node) {
    if (!node) return;
    
    /* Emit prologue */
    fprintf(gen->output, ".section .text\n");
    fprintf(gen->output, ".globl _start\n");
    codegen_label(gen, "_start");
    
    /* Set up stack frame */
    codegen_emit(gen, "push rbp");
    codegen_emit(gen, "mov rbp, rsp");
    
    /* Generate statements */
    for (int i = 0; i < node->data.program.count; i++) {
        codegen_stmt(gen, node->data.program.stmts[i]);
    }
    
    /* Exit */
    codegen_emit(gen, "mov rax, 60");  /* sys_exit */
    codegen_emit(gen, "xor edi, edi");  /* exit code 0 */
    codegen_emit(gen, "syscall");
}

/* Initialize code generator */
void codegen_init(CodeGen *gen, FILE *output) {
    gen->output = output;
    gen->label_count = 0;
    gen->stack_offset = 0;
    gen->locals_count = 0;
    memset(gen->locals, 0, sizeof(gen->locals));
}

/* Main function */
int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <input.py> [output.s]\n", argv[0]);
        return 1;
    }
    
    /* Read input file */
    FILE *input = fopen(argv[1], "r");
    if (!input) {
        fprintf(stderr, "Error: Cannot open input file: %s\n", argv[1]);
        return 1;
    }
    
    fseek(input, 0, SEEK_END);
    long size = ftell(input);
    fseek(input, 0, SEEK_SET);
    
    char *source = (char *)malloc(size + 1);
    fread(source, 1, size, input);
    source[size] = '\0';
    fclose(input);
    
    /* Open output file */
    FILE *output;
    if (argc >= 3) {
        output = fopen(argv[2], "w");
    } else {
        output = fopen("output.s", "w");
    }
    
    if (!output) {
        fprintf(stderr, "Error: Cannot open output file\n");
        free(source);
        return 1;
    }
    
    /* Emit header */
    fprintf(output, "# Generated by CustomPython Autocompiler\n");
    fprintf(output, "# Input: %s\n", argv[1]);
    fprintf(output, "\n");
    fprintf(output, ".section .data\n");
    fprintf(output, "format_int: .string \"%%ld\\n\"\n");
    fprintf(output, "format_str: .string \"%%s\\n\"\n");
    fprintf(output, "\n");
    
    /* Initialize code generator */
    CodeGen gen;
    codegen_init(&gen, output);
    
    /* Initialize lexer */
    Lexer lex;
    lexer_init(&lex, source);
    
    /* Simple parser for testing */
    fprintf(output, ".section .text\n");
    fprintf(output, ".globl _start\n");
    codegen_label(&gen, "_start");
    
    /* Prologue */
    codegen_emit(&gen, "push rbp");
    codegen_emit(&gen, "mov rbp, rsp");
    
    /* Example: simple expression */
    codegen_number(&gen, 42);
    codegen_emit(&gen, "lea rdi, [rip + format_int]");
    codegen_emit(&gen, "mov rsi, rax");
    codegen_emit(&gen, "xor eax, eax");
    codegen_emit(&gen, "call printf");
    
    /* Exit */
    codegen_emit(&gen, "mov rax, 60");
    codegen_emit(&gen, "xor edi, edi");
    codegen_emit(&gen, "syscall");
    
    /* Cleanup */
    fclose(output);
    free(source);
    
    printf("Assembly generated successfully: %s\n", argc >= 3 ? argv[2] : "output.s");
    return 0;
}
