package ControllerLoop;

import java.util.Scanner;

public class BreakDemo02 {
    public static void main(String[] args) {
        /*
        键盘录入一个大于等于 2 的整数，判断是否为质数。 

        质数：只能被 1 和它本身整除的整数，且大于 1。
        例如：2、3、5、7、11、13、17、19、23、29、31 等。
        */
       Scanner sc = new Scanner(System.in);
       int num = 0;
       while (true) {
            System.out.println("请输入一个大于等于 2 的整数：");
            num = sc.nextInt();
            if (num >= 2) {
                break;
            }else{
                System.out.println("请输入一个大于等于 2 的整数！");
            }
       }
       
       // 判断 num 记录的数据，是否为一个质数
       int count = 0;
       for (int i = 2; i <= num - 1; i++) {
            if (num % i == 0) {
                count++;
                System.out.println("该整数不是质数！");
                break;
            }
       }
       
       // 判断 count 是否为 0
       if (count == 0) {
            System.out.println("该整数为质数！");
       }else{
            System.out.println("该整数不是质数！");
       }
       sc.close();       
    }
}
