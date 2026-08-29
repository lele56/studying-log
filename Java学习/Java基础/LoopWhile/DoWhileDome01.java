package LoopWhile;

public class DoWhileDome01 {
    public static void main(String[] args) {
        /*
        利用 do...while 循环，输出 5 行“hello world”
        注：do...while 循环，熟悉语法即可，无需额外练习。
        特点：先执行后判断，循环体至少执行一次。
        for，while 的特点，先判断后执行。
        */
        int i = 0;
        do {
            System.out.println("hello world");
            i++;
        } while (i <= 5);
    }
}
