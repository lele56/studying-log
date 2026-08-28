package LoopFor;

public class ForDemo02 {
    public static void main(String[] args) {
        /*
        需求：求 1~5 的和
        */
        int sum = 0;
        for (int i = 1; i <= 5; i++) {
            sum += i;
        }
        System.out.println("1~5 的和为：" + sum);
    }
}
