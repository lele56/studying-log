package Polymorphic;

/**
 * 学生类（继承 Person）
 * 
 * 重写 work() 方法：学生的工作是学习
 * 体现了多态：同一个方法名，不同子类有不同实现
 */
public class Student extends Person {

    public Student() {
        super();
    }

    public Student(String name, String username, String password) {
        super(name, username, password);
    }

    /**
     * 重写父类的 work() 方法
     * 学生的工作是学习
     */
    @Override
    public void work() {
        System.out.println(getName() + " 学生的工作是学习");
    }

    /**
     * 重写父类的 getRole() 方法
     * 返回具体的角色名
     */
    @Override
    public String getRole() {
        return "学生";
    }
}