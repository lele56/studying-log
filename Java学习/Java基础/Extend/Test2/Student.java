package Extend.Test2;

/**
 * 学生类（中间层：继承 Person，被 UndergradStudent 和 MasterStudent 继承）
 * 
 * 继承链：Object → Person → Student → UndergradStudent / MasterStudent
 * 
 * 作为中间层的角色：
 * 1. 继承父类（Person）的属性和方法
 * 2. 添加自己的特有属性（grade）
 * 3. 为子类（UndergradStudent、MasterStudent）提供公共方法（learn）
 */
public class Student extends Person {
    // ==================== 特有属性 ====================
    private String grade;  // 年级，如：大二、研一

    // ==================== 构造方法 ====================
    public Student() {
        super();
    }

    public Student(String name, int age, String grade) {
        super(name, age);
        this.grade = grade;
    }

    // ==================== Getter/Setter ====================
    public String getGrade() {
        return grade;
    }

    public void setGrade(String grade) {
        this.grade = grade;
    }

    // ==================== 特有方法 ====================
    /**
     * 学习方法
     * 子类（UndergradStudent、MasterStudent）会重写此方法
     */
    public void learn() {
        System.out.println(getName() + " 正在学习");
    }

    // ==================== 重写父类方法 ====================
    @Override
    public void eat() {
        System.out.println(getName() + " 飞快地吃完饭，赶去上课！");
    }

    @Override
    public void showInfo() {
        super.showInfo();  // 调用 Person 的 showInfo
        System.out.println("年级：" + grade);
    }
}