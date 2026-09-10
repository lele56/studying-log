package Polymorphic;

/**
 * 管理员类（继承 Person）
 * 
 * 重写 work() 方法：管理员的工作是管理网站
 */
public class Admin extends Person {

    public Admin() {
        super();
    }

    public Admin(String name, String username, String password) {
        super(name, username, password);
    }

    /**
     * 重写父类的 work() 方法
     * 管理员的工作是管理网站
     */
    @Override
    public void work() {
        System.out.println(getName() + " 管理员的工作是管理网站");
    }

    /**
     * 重写父类的 getRole() 方法
     */
    @Override
    public String getRole() {
        return "管理员";
    }
}