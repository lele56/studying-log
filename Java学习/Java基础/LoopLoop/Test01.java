package LoopLoop;

public class Test01 {
    public static void main(String[] args) {
        /*
        打印 4 行 5 列的 *
        ******
        ******
        ******
        ******
        */
        // System.out.println("*") 先打印，再换行
        // System.out.print("*") 只打印，不换行
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 5; j++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
}
