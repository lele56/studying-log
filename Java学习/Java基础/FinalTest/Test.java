package FinalTest;

public class Test {
    public static void main(String[] args) {
        /*
         * final 修饰变量，此时叫做常量
         * 特点1：只能被赋值一次，一旦赋值，无法再次修改。
         * 特点2：常量名大写，多个单词之间用下划线隔开
         * 
         * 细节：
         *      基本数据类型：
         *          byte short int long float double char boolean
         *          变量里面记录的是真实的数据
         *          final int a = 10；此时变量里面记录的数据无法发生改变
         *      引用数据类型：
         *          除了上面四类八种，其他所有的数据类型都是引用类型
         *          int[] student....
         *          变量里面记录的是引用地址
         *      综上所述：
         *          final 修饰哪个变量，这个变量里面记录的内容就无法再次发生改变
         * 
         */
        // 1. 定义一个常量
        final int NUMBER = 100;

        // 2. 调用常量
        System.out.println(NUMBER);
    }
}
