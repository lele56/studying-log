package Extend.Test1;

/**
 * 教师类（子类/派生类）
 * 继承 Person 类，拥有 Person 的所有属性和方法
 * 
 * 继承链：
 * Object → Person → Teacher
 * 
 * 注意：Java 是单继承，Teacher 不能同时继承 Person 和另一个类
 * 但可以通过实现接口（implements）来弥补单继承的限制
 */
public class Teacher extends Person {
    // ==================== 特有属性 ====================
    private String subject;  // 教授的科目，如：数学、英语

    // ==================== 构造方法 ====================
    /**
     * 无参构造
     */
    public Teacher() {
        super();
    }

    /**
     * 有参构造
     * 
     * @param name    姓名
     * @param age     年龄
     * @param subject 教授的科目
     */
    public Teacher(String name, int age, String subject) {
        super(name, age);  // 调用父类有参构造
        this.subject = subject;
    }

    // ==================== Getter/Setter ====================
    public String getSubject() {
        return subject;
    }

    public void setSubject(String subject) {
        this.subject = subject;
    }

    // ==================== 特有方法 ====================
    /**
     * 教师教学的方法（子类特有的方法）
     */
    public void teach() {
        System.out.println(getName() + " 老师正在教 " + subject + "...");
    }

    /**
     * 批改作业的方法
     */
    public void gradeHomework() {
        System.out.println(getName() + " 老师正在批改作业...");
    }

    // ==================== 重写父类方法 ====================
    /**
     * 重写父类的 showInfo 方法
     */
    @Override
    public void showInfo() {
        super.showInfo();
        System.out.println("科目：" + subject);
    }

    /**
     * 重写父类的 eat 方法
     * 老师吃饭也很匆忙！
     */
    @Override
    public void eat() {
        System.out.println(getName() + " 老师匆匆吃完饭，赶去上课！");
    }
}