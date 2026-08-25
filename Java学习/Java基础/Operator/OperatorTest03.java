package Operator;

public class OperatorTest03 {
    public static void main(String[] args) {

        // 练习一：
        byte b = 100;
        short s = 200;
        double d = 20.3;

        /*
        byte 类型和 short 类型相加时，会先把它们转换成 int 类型，
        int 类型和 double 类型相加时，会把 int 类型转换成 double 类型
        */
        double result1 = b + s + d;
        System.out.println(result1); // 320.3

        // 练习二：
        short s1 = 100;
        short s2 = 200;
        
        // short > byte
        // 所以，s1 + s2 会先把 s1 和 s2 转换成 int 类型，再相加
        // 最后把 int 类型转换成 byte 类型
        // 330 ：二进制为 00000010 00101010
        // 强制转换 byte：00101010（44）
        byte result2 = (byte)(s1 + s2); 
        System.out.println(result2); // 44
    }
}
