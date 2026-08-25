package Operator;

import java.util.Scanner;

public class OperatorTest04 {
    public static void main(String[] args) {
        // 实现字母的大小写转换，将大写字母转换为小写字母
        // A -> a
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入一个字母：");
        char c = sc.next().charAt(0);
        System.out.println("转换结果：" + convert(c));
        sc.close();
    }

    public static char convert(char c) {
        if (c >= 'A' && c <= 'Z') {
            return (char)(c + 32);
        } else {
            return c;
        }
    }
}
