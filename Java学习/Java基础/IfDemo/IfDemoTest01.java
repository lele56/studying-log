package IfDemo;

import java.util.Scanner;

public class IfDemoTest01 {
    public static void main(String[] args) {
        /*
        需求：
            初始最大生命200，受到x点伤害，技能恢复y点血，x和y由键盘录入而来
            假设游戏人物不会死亡，最少1点血
        问：最终游戏人物血量是多少？
        */
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入受到的伤害值：");
        int x = sc.nextInt();
        System.out.println("请输入技能恢复的血量：");
        int y = sc.nextInt();
        int max = 200;
        int finalHp = getInjure(max, x);
        finalHp = getRecover(finalHp, y);
        System.out.println("最终游戏人物血量为：" + finalHp);
        sc.close();
    }

    public static int getInjure(int hp, int x) {
        return (hp - x) > 0 ? (hp - x) : 1;
    }
    public static int getRecover(int hp, int y) {
        return hp + y;
    }
}
