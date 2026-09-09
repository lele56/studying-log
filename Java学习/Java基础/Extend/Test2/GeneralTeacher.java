package Extend.Test2;

/**
 * 通识课教师类（底层子类）
 * 
 * 继承链：Object → Person → Teacher → GeneralTeacher
 * 
 * 通识课教师：教授全校公共通识课（如大学英语、思政等）
 */
public class GeneralTeacher extends Teacher {

    // ==================== 构造方法 ====================
    public GeneralTeacher() {
        super();
    }

    public GeneralTeacher(String name, int age, String subject) {
        super(name, age, subject);
    }

    // ==================== 重写父类 Teacher 的方法 ====================
    @Override
    public void teach() {
        super.teach();  // 调用 Teacher 的 teach()
        System.out.println("  → 通识课教师正在教授面向全校的通识课知识");
    }

    // ==================== 重写"爷爷类" Person 的方法 ====================
    @Override
    public void showInfo() {
        super.showInfo();  // 调用 Teacher 的 showInfo
        System.out.println("类型：通识课教师");
    }

    @Override
    public void eat() {
        System.out.println(getName() + " 老师在教职工食堂快速吃饭！");
    }
}