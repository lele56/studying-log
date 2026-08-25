package IfDemo;

public class IfDemoTest02 {
    public static void main(String[] args) {
        /* 
         * if 的细节： 
         *     1. if 语句大括号的位置 
         *         左括号写在上一行的末尾，不要单独写一行 
         *         K&R风格（紧凑风），左括号在上一行的末尾 
         *         Allman风格（换行风），左括号在下一行的开头 
         * 
         *     2. if 语句大括号的省略 
         *         如果 if 语句只有一条语句，可以省略大括号 
         * 
         *     3. 小括号后面不能有分号 
         *         小括号后面不能有分号，只要会拆开 if 的语句结构 
         * 
         *     4. 判断布尔类型的变量 
         *         如果判断的变量是布尔类型，直接把变量写在小括号中即可 
         */

        int age = 20;

        // 1. 大括号的位置
        // K&R 风格（Java 官方推荐）
        if (age >= 18) {
            System.out.println("K&R 风格：成年了");
        }

        // Allman 风格（虽然能跑，但 Java 中很少用）
        if (age >= 18)
        {
            System.out.println("Allman 风格：成年了");
        }

        // 2. 大括号的省略
        // 只有一行代码时可以省略，但不推荐（容易在后续维护时出错）
        if (age >= 18)
            System.out.println("省略大括号：成年了");

        // 3. 小括号后面不能有分号
        // 错误示范：if (age >= 18); 
        // 解释：分号代表一个空语句，if 判断完就结束了。
        // 下面的大括号块就变成了独立代码块，无论条件是否满足都会执行！
        /*
        if (age >= 18); {
            System.out.println("这是一个坑！这行代码永远会被执行");
        }
        */

        // 4. 判断布尔类型的变量
        boolean isAdult = true;

        // 推荐写法：直接写变量名
        if (isAdult) {
            System.out.println("推荐写法：是成年人");
        }

        // 不推荐写法：多余地比较 true
        if (isAdult == true) {
            System.out.println("不推荐写法：是成年人");
        }
    }
}