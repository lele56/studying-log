package ControllerLoop;

public class BreakDemo01 {
    public static void main(String[] args) {
        /*
        break 关键字：
            不能单独出现的，只能写在 switch 或循环当中，表示结束、跳出的意思。
        */
        for (int i = 0; i < 10; i++) {
            if (i == 5) {
                break;
            }
            System.out.println(i);
        }
    }
}
