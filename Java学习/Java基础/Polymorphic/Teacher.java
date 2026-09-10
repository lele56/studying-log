package Polymorphic;

/**
 * 教师类（继承 Person）
 * 
 * 重写 work() 方法：教师的工作是教学
 */
public class Teacher extends Person {

    public Teacher() {
        super();
    }

    public Teacher(String name, String username, String password) {
        super(name, username, password);
    }

    /**
     * 重写父类的 work() 方法
     * 教师的工作是教学
     */
    @Override
    public void work() {
        System.out.println(getName() + " 教师的工作是教学");
    }

    /**
     * 重写父类的 getRole() 方法
     */
    @Override
    public String getRole() {
        return "教师";
    }
}