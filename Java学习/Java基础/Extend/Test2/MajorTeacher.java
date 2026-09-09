package Extend.Test2;

/**
 * 专业课教师类（底层子类）
 * 
 * 继承链：Object → Person → Teacher → MajorTeacher
 * 
 * 专业课教师：教授本专业的核心课程
 */
public class MajorTeacher extends Teacher {

    // ==================== 构造方法 ====================
    public MajorTeacher() {
        super();
    }

    public MajorTeacher(String name, int age, String subject) {
        super(name, age, subject);
    }

    // ==================== 重写父类 Teacher 的方法 ====================
    @Override
    public void teach() {
        super.teach();  // 调用 Teacher 的 teach()
        System.out.println("  → 专业课教师正在教授本专业的核心课程");
    }

    // ==================== 重写"爷爷类" Person 的方法 ====================
    @Override
    public void showInfo() {
        super.showInfo();  // 调用 Teacher 的 showInfo
        System.out.println("类型：专业课教师");
    }

    @Override
    public void eat() {
        System.out.println(getName() + " 老师在办公室边备课边吃饭！");
    }
}