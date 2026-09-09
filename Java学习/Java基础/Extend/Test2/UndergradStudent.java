package Extend.Test2;

/**
 * 本科学生类（底层子类）
 * 
 * 继承链：Object → Person → Student → UndergradStudent
 * 
 * 三层继承的特点：
 * 1. 可以调用"爷爷类" Person 的方法：getName()、getAge()、sleep()
 * 2. 可以调用"父亲类" Student 的方法：getGrade()
 * 3. 可以重写"父亲类" Student 的方法：learn()
 * 4. 可以重写"爷爷类" Person 的方法：eat()、showInfo()
 */
public class UndergradStudent extends Student {

    // ==================== 构造方法 ====================
    public UndergradStudent() {
        super();
    }

    public UndergradStudent(String name, int age, String grade) {
        super(name, age, grade);
    }

    // ==================== 重写父类 Student 的方法 ====================
    @Override
    public void learn() {
        // super.learn() 调用 Student 的 learn()，再追加自己的内容
        super.learn();
        System.out.println("  → 本科生正在攻读学士学位...");
    }

    // ==================== 重写"爷爷类" Person 的方法 ====================
    @Override
    public void showInfo() {
        super.showInfo();  // 调用 Student 的 showInfo（Student 又调用了 Person 的 showInfo）
        System.out.println("学历：本科生（学士学位）");
    }

    @Override
    public void eat() {
        System.out.println(getName() + "（本科生）在食堂快速吃饭！");
    }
}