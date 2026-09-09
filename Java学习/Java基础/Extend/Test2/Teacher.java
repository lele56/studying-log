package Extend.Test2;

/**
 * 教师类（中间层：继承 Person，被 GeneralTeacher 和 MajorTeacher 继承）
 * 
 * 继承链：Object → Person → Teacher → GeneralTeacher / MajorTeacher
 */
public class Teacher extends Person {
    // ==================== 特有属性 ====================
    private String subject;  // 教授的科目

    // ==================== 构造方法 ====================
    public Teacher() {
        super();
    }

    public Teacher(String name, int age, String subject) {
        super(name, age);
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
     * 教学方法
     * 子类（GeneralTeacher、MajorTeacher）会重写此方法
     */
    public void teach() {
        System.out.println(getName() + " 老师正在教 " + subject);
    }

    // ==================== 重写父类方法 ====================
    @Override
    public void eat() {
        System.out.println(getName() + " 老师匆匆吃完午饭，继续备课！");
    }

    @Override
    public void showInfo() {
        super.showInfo();  // 调用 Person 的 showInfo
        System.out.println("科目：" + subject);
    }
}