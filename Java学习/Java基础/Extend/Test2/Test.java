package Extend.Test2;

/**
 * 测试类：演示三层继承 + 多态
 * 
 * 继承体系：
 * 
 *                     Person（顶层父类）
 *                    /     \
 *           Student       Teacher（中间层）
 *          /      \       /      \
 *  Undergrad  Master  General  Major（底层子类）
 * 
 * 三层继承演示：
 * 1. 底层子类可以调用"爷爷类" Person 的方法
 * 2. super.learn() 调用的是"父亲类" Student 的方法
 * 3. 多态：Person 类型的变量可以指向任何子类对象
 * 4. instanceof 和向下转型
 */
public class Test {
    public static void main(String[] args) {

        // ==================== 1. 创建对象 ====================
        System.out.println("==================== 1. 创建对象 ====================");
        UndergradStudent ugs = new UndergradStudent("小明", 20, "大二");
        MasterStudent ms = new MasterStudent("小红", 24, "研一");
        GeneralTeacher gt = new GeneralTeacher("张老师", 35, "大学英语");
        MajorTeacher mt = new MajorTeacher("王老师", 40, "数据结构");

        // ==================== 2. 三层调用链：super 逐层向上 ====================
        System.out.println("\n==================== 2. 三层调用链 ====================");
        // 调用 learn() → UndergradStudent.learn() 中 super.learn() → Student.learn()
        System.out.println("--- 本科生学习 ---");
        ugs.learn();
        System.out.println("\n--- 研究生学习 ---");
        ms.learn();

        // 调用 teach() → GeneralTeacher.teach() 中 super.teach() → Teacher.teach()
        System.out.println("\n--- 通识课教师教学 ---");
        gt.teach();
        System.out.println("\n--- 专业课教师教学 ---");
        mt.teach();

        // ==================== 3. 调用"爷爷类"的方法 ====================
        System.out.println("\n==================== 3. 底层子类调用\"爷爷类\"方法 ====================");
        // UndergradStudent 的爷爷类是 Person，可以直接调用 Person 的方法
        ugs.sleep();  // 继承自 Person
        mt.sleep();   // 继承自 Person
        System.out.println("本科生姓名：" + ugs.getName());  // getName() 继承自 Person
        System.out.println("专业课教师姓名：" + mt.getName());

        // ==================== 4. 多态：父类引用指向子类对象 ====================
        System.out.println("\n==================== 4. 多态 ====================");
        Person[] people = { ugs, ms, gt, mt };

        // 统一调用 eat()，实际执行各自重写后的版本
        for (Person p : people) {
            p.eat();
        }

        // ==================== 5. showInfo 多态调用 ====================
        System.out.println("\n==================== 5. showInfo 多态 ====================");
        for (Person p : people) {
            p.showInfo();
            System.out.println("---");
        }

        // ==================== 6. instanceof 判断 + 向下转型 ====================
        System.out.println("\n==================== 6. instanceof 判断类型 ====================");
        for (Person p : people) {
            if (p instanceof UndergradStudent) {
                UndergradStudent u = (UndergradStudent) p;
                System.out.println(u.getName() + " 是本科生，年级：" + u.getGrade());
            } else if (p instanceof MasterStudent) {
                MasterStudent m = (MasterStudent) p;
                System.out.println(m.getName() + " 是研究生，年级：" + m.getGrade());
            } else if (p instanceof GeneralTeacher) {
                GeneralTeacher g = (GeneralTeacher) p;
                System.out.println(g.getName() + " 是通识课教师，科目：" + g.getSubject());
            } else if (p instanceof MajorTeacher) {
                MajorTeacher maj = (MajorTeacher) p;
                System.out.println(maj.getName() + " 是专业课教师，科目：" + maj.getSubject());
            }
        }
    }
}