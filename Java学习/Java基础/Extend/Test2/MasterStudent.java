package Extend.Test2;

/**
 * 硕士学生类（底层子类）
 * 
 * 继承链：Object → Person → Student → MasterStudent
 * 
 * 与 UndergradStudent 是兄弟类，都继承自 Student
 */
public class MasterStudent extends Student {

    // ==================== 构造方法 ====================
    public MasterStudent() {
        super();
    }

    public MasterStudent(String name, int age, String grade) {
        super(name, age, grade);
    }

    // ==================== 重写父类 Student 的方法 ====================
    @Override
    public void learn() {
        super.learn();  // 调用 Student 的 learn()
        System.out.println("  → 研究生正在攻读硕士学位...");
    }

    // ==================== 重写"爷爷类" Person 的方法 ====================
    @Override
    public void showInfo() {
        super.showInfo();  // 调用 Student 的 showInfo
        System.out.println("学历：硕士研究生（硕士学位）");
    }

    @Override
    public void eat() {
        System.out.println(getName() + "（研究生）在实验室边吃边做实验！");
    }
}