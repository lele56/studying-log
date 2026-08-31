package ControllerLoop;

public class ContinueDemo01 {
    public static void main(String[] args) {
        /*
        循环打印 1~100 之间的数字，如果数字包含 7 或者是 7 的倍数，就输出"过"
        */
        for (int i = 1; i <= 100; i++) {
            int ge = i % 10;
            int shi = i / 10;
            
            if (ge == 7 || shi == 7 || i % 7 == 0) {
                System.out.println("过");
                continue;
            } else {
                System.out.println(i);
            }
        }
    }
}

