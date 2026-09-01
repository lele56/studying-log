package Method;

public class MethodDemo01 {
    public static void main(String[] args) {
        /*
        练习：定义一个方法，求两数之和

        定义格式：
            public static void 方法名(参数类型 参数名, 参数类型 参数名) {
                方法体
                return 返回值
            }
        
        调用格式：
            方法名(参数值, 参数值);    

        注意点：
            1. 方法跟方法之间是平级关系，不能嵌套定义。
            2. 方法不会主动运行的，需要被调用才可以
            3. 小括号中的参数需要一一对应（个数，类型）
        */
        // 1. 调用方法
        int result = sum(10, 20);
        System.out.println(result);
    }

    public static int sum(int a, int b) {
        return a + b;
    }
}
