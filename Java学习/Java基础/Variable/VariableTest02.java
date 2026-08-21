// 街头霸王
public class Test02 {
    public static void main(String[] args) {
        /*
        我方：叉子             对方：长手
        攻击：220              攻击：210
        防御：85               防御：80
        血量：1012.5           血量：1223.3
        技能加成：1.2          技能加成：1.3
        
        技能造成的伤害的公式：攻击力 * 技能加成 - 防御力 
        普攻造成的伤害的公式：攻击力 - 防御力

        计算：
            我方第一次进行普通攻击，造成多少伤害，对方还剩余多少血量？
            我方第二次进行技能攻击，造成多少伤害，对方还剩余多少血量？
        */
        // 创建玩家对象
        Player player1 = new Player("叉子", 220, 85, 1012.5, 1.2);
        Player player2 = new Player("长手", 210, 80, 1223.3, 1.3);
        
        // 第一次进行普通攻击
        double normalDamage = player1.calcNormalDamage(player2);
        System.out.println(player1.name + "第一次普通攻击，造成伤害：" + normalDamage);
        // 第一次普通普通攻击后，对方还剩余多少血量
        player2.hp -= normalDamage;
        System.out.println(player2.name + "还剩余血量：" + player2.hp);

        // 第二次进行技能攻击
        double skillDamage = player1.calcSkillDamage(player2);
        System.out.println(player1.name + "第二次技能攻击，造成伤害：" + skillDamage);
        // 第二次技能技能攻击后，对方还剩余多少血量
        player2.hp -= skillDamage;
        System.out.println(player2.name + "还剩余血量：" + player2.hp);
        
    }
}

class Player {
    // 定义属性
    String name;              // 名字
    int attack;               // 攻击力
    int defense;              // 防御力
    double hp;                // 血量
    double skillMultiplier;   // 技能加成

    // 构造方法：和类名同名，没有返回值
    public Player(String name, int attack, int defense, double hp, double skillMultiplier) {
        this.name = name;
        this.attack = attack;
        this.defense = defense;
        this.hp = hp;
        this.skillMultiplier = skillMultiplier;
    }

    // 计算普攻伤害
    public double calcNormalDamage(Player target){
        return attack - target.defense;
    }
    
    // 计算技能伤害
    public double calcSkillDamage(Player target){
        return attack * skillMultiplier - target.defense;
    }
}
