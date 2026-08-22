package Variable;

public class VariableTest03 {
    public static void main(String[] args) {
        /*
        定义8种数据类型的变量
        
        整数类型：byte、short、int、long
        浮点数类型：float、double
        字符类型：char
        布尔类型：boolean

        变量的定义格式：
                数据类型 变量名 = 值;
        */

       // 1. 定义byte类型的变量
       byte a = 127;
       System.out.println(a);

       // 2. 定义short类型的变量
       short b = 32767;
       System.out.println(b);

       // 3. 定义int类型的变量
       int c = 2147483647;
       System.out.println(c);
        
       // 4. 定义long类型的变量
       // 注意：long类型的变量需要在值后添加 L 或 l
       // 因为 int 类型的默认值是 int 类型，所以需要添加 L 或 l 来指定是 long 类型
       // 建议：一般写成大写的
       long d = 9223372036854775807L;
       System.out.println(d);

       // 5. 定义float类型的变量
       // 注意：float类型的变量需要在值后添加 f 或者 F
       // 建议：一般写成大写的
       float e = 3.14f;
       System.out.println(e);

       // 6. 定义double类型的变量
       double f = 3.1415926;
       System.out.println(f);

       // 7. 定义char类型的变量
       // 注意：引号中间只能放一个字符
       char g = 'a';
       System.out.println(g);

       // 8. 定义boolean类型的变量
       boolean h = true;
       System.out.println(h);

       /*
        * 📊 8种基本数据类型一览表：
        * -------------------------------------------------------
        * 分类       | 类型    | 内存占用 | 取值范围
        * -------------------------------------------------------
        * 整数型     | byte    | 1 字节   | -128 ~ 127
        *           | short   | 2 字节   | -32,768 ~ 32,767
        *           | int     | 4 字节   | -21亿 ~ 21亿 (最常用)
        *           | long    | 8 字节   | 极大 (约 ±9×10¹⁸)
        * -------------------------------------------------------
        * 浮点型     | float   | 4 字节   | 约 ±3.4×10³⁸ (需加 f)
        *           | double  | 8 字节   | 约 ±1.7×10³⁰⁸ (最常用)
        * -------------------------------------------------------
        * 字符型     | char    | 2 字节   | 0 ~ 65,535 (支持中文)
        * 布尔型     | boolean | 视JVM而定 | true / false
        * -------------------------------------------------------
        * 
        * 💡 记忆技巧：
        * 1. byte(1) -> short(2) -> int(4) -> long(8)
        * 2. float(4) -> double(8)
        * 3. char(2) -> 因为要存中文等万国码，所以比 byte 大
        * 4. 整数默认 int，小数默认 double
        */

    }
}