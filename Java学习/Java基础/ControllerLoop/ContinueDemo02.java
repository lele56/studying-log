package ControllerLoop;

import java.util.Random;
import java.util.Scanner;

public class ContinueDemo02 {
    public static void main(String[] args) {
        /*
        生成一个 1~100 之间的随机数，利用键盘录入模拟猜的动作，一直猜，直到猜中
        */
        Scanner sc = new Scanner(System.in);
        Random rd = new Random();
        int random = rd.nextInt(100) + 1;
        int count = 0;
        
        while (true) {
            System.out.print("请输入你猜的数字（1~100）：");
            
            if (!sc.hasNextInt()) {
                System.out.println("请输入有效的整数！\n");
                sc.next();
                continue;
            }
            
            int guess = sc.nextInt();
            count++;
            
            if (guess == random) {
                System.out.println("恭喜你猜对了！共猜了 " + count + " 次");
                break;
            } else if (guess < random) {
                System.out.println("猜小了！请重新输入\n");
            } else {
                System.out.println("猜大了！请重新输入\n");
            }
        }
        
        sc.close();
    }
}