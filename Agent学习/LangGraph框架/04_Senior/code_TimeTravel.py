import uuid

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, NotRequired

class StoryState(TypedDict):
    """故事状态：字段均可逐步写入。"""

    character: NotRequired[str]
    setting: NotRequired[str]
    plot: NotRequired[str]
    ending: NotRequired[str]

def create_character(state: StoryState):
    """创建故事角色（模拟 LLM 节点）。"""
    print("执行节点: create_character")

    mock_character = "一只会说话的猫"
    print(f"创建的角色: {mock_character}")
    return {"character": mock_character}

def set_setting(state: StoryState):
    """设置故事背景。"""
    print("执行节点: set_setting")

    mock_setting = "在一个神秘的图书馆里"
    print(f"设置的背景: {mock_setting}")
    return {"setting": mock_setting}

def develop_plot(state: StoryState):
    """发展故事情节。"""
    print("执行节点: develop_plot")

    character = state.get("character", "未知角色")
    setting = state.get("setting", "未知背景")
    mock_plot = f"{character}在{setting}发现了一本会发光的书"
    print(f"发展的剧情: {mock_plot}")
    return {"plot": mock_plot}

def write_ending(state: StoryState):
    """编写故事结局。"""
    print("执行节点: write_ending")

    plot = state.get("plot", "未知剧情")
    mock_ending = f"当{plot}时，整个图书馆都被魔法光芒照亮了"
    print(f"编写的结局: {mock_ending}")
    return {"ending": mock_ending}

def main():
    print("=== LangGraph 高级时间旅行演示 ===\n")

    workflow = StateGraph(StoryState)

    workflow.add_node("create_character", create_character)
    workflow.add_node("set_setting", set_setting)
    workflow.add_node("develop_plot", develop_plot)
    workflow.add_node("write_ending", write_ending)

    workflow.add_edge(START, "create_character")
    workflow.add_edge("create_character", "set_setting")
    workflow.add_edge("set_setting", "develop_plot")
    workflow.add_edge("develop_plot", "write_ending")
    workflow.add_edge("write_ending", END)

    graph = workflow.compile(checkpointer=InMemorySaver())

    print("1. 生成第一个故事...")
    config1 = {
        "configurable": {
            "thread_id": str(uuid.uuid4()),
        }
    }

    story1 = graph.invoke({}, config1)
    print(f"角色: {story1['character']}")
    print(f"背景: {story1['setting']}")
    print(f"剧情: {story1['plot']}")
    print(f"结局: {story1['ending']}")
    print("话痨猫-图书馆-发光书-魔法亮")
    print()

    print("2. 查看第一个故事的历史状态...")

    states1 = list(graph.get_state_history(config1))

    print("历史状态:")
    for i, state in enumerate(states1):
        print(f"  {i}. 下一步节点: {state.next}")
        print(f"     检查点ID: {state.config['configurable']['checkpoint_id']}")
        if state.values:
            print(f"     状态值: {state.values}")
        print()

    print("3. 从中间状态恢复执行，创建第二个故事...")

    # 索引需与 get_state_history 顺序一致；states1[2] 对应 create_character 执行后的快照（请以本地打印为准调整）
    character_state = states1[2]
    print(f"选中的状态: {character_state.next}")
    print(f"选中的状态值: {character_state.values}")

    new_config = graph.update_state(
        character_state.config,
        values={"character": "一只会飞的龙"},
    )

    print(f"新配置: {new_config}")
    print()

    print("4. 从新检查点恢复执行，生成第二个故事...")
    story2 = graph.invoke(None, new_config)
    print(f"新角色: {story2['character']}")
    print(f"背景: {story2['setting']}")
    print(f"剧情: {story2['plot']}")
    print(f"结局: {story2['ending']}")
    print()

    print("5. 比较两个故事:")
    print("  故事1:")
    print(f"    角色: {story1['character']}")
    print(f"    背景: {story1['setting']}")
    print(f"    剧情: {story1['plot']}")
    print(f"    结局: {story1['ending']}")
    print()

    print("  故事2:")
    print(f"    角色: {story2['character']}")
    print(f"    背景: {story2['setting']}")
    print(f"    剧情: {story2['plot']}")
    print(f"    结局: {story2['ending']}")
    print()

    print("=== 演示完成 ===")


if __name__ == "__main__":
    main()

"""
【输出示例】
=== LangGraph 高级时间旅行演示 ===

1. 生成第一个故事...
执行节点: create_character
创建的角色: 一只会说话的猫
执行节点: set_setting
设置的背景: 在一个神秘的图书馆里
执行节点: develop_plot
发展的剧情: 一只会说话的猫在在一个神秘的图书馆里发现了一本会发光的书
执行节点: write_ending
编写的结局: 当一只会说话的猫在在一个神秘的图书馆里发现了一本会发光的书时，整个图书馆都被魔法光芒照亮了
角色: 一只会说话的猫
背景: 在一个神秘的图书馆里
剧情: 一只会说话的猫在在一个神秘的图书馆里发现了一本会发光的书
结局: 当一只会说话的猫在在一个神秘的图书馆里发现了一本会发光的书时，整个图书馆都被魔法光芒照亮了
话痨猫-图书馆-发光书-魔法亮

2. 查看第一个故事的历史状态...
历史状态:
  0. 下一步节点: ()
     检查点ID: 1f1a768d-a7c8-6387-8004-85e8f1dc38fe
     状态值: {'character': '一只会说话的猫', 'setting': '在一个神秘的图书馆里', 'plot': '一只会说话的猫在在一个神秘的图书馆里发现了一本会发光的书', 'ending': '当一只会说话的猫在在一个神秘的图书馆里发现了一本会发光的书时，整个图书馆都被魔法光芒照亮了'}

  1. 下一步节点: ('write_ending',)
     检查点ID: 1f1a768d-a7c8-6386-8003-064c4056d497
     状态值: {'character': '一只会说话的猫', 'setting': '在一个神秘的图书馆里', 'plot': '一只会说话的猫在在一个神秘的图书馆里发现了一本会发光的书'}

  2. 下一步节点: ('develop_plot',)
     检查点ID: 1f1a768d-a7c2-630a-8002-d366419d7892
     状态值: {'character': '一只会说话的猫', 'setting': '在一个神秘的图书馆里'}

  3. 下一步节点: ('set_setting',)
     检查点ID: 1f1a768d-a7c2-6309-8001-ddcb4b58d885
     状态值: {'character': '一只会说话的猫'}

  4. 下一步节点: ('create_character',)
     检查点ID: 1f1a768d-a7c0-6588-8000-3ff0ce4c9a85

  5. 下一步节点: ('__start__',)
     检查点ID: 1f1a768d-a7b5-67bc-bfff-7abee7acc6f8

3. 从中间状态恢复执行，创建第二个故事...
选中的状态: ('develop_plot',)
选中的状态值: {'character': '一只会说话的猫', 'setting': '在一个神秘的图书馆里'}
新配置: {'configurable': {'thread_id': '59761ea1-c4d8-4000-bb16-e754c7c9d645', 'checkpoint_ns': '', 'checkpoint_id': '1f1a768d-a7d4-6dec-8003-67381039c9dd'}}

4. 从新检查点恢复执行，生成第二个故事...
执行节点: develop_plot
发展的剧情: 一只会飞的龙在在一个神秘的图书馆里发现了一本会发光的书
执行节点: write_ending
编写的结局: 当一只会飞的龙在在一个神秘的图书馆里发现了一本会发光的书时，整个图书馆都被魔法光芒照亮了
新角色: 一只会飞的龙
背景: 在一个神秘的图书馆里
剧情: 一只会飞的龙在在一个神秘的图书馆里发现了一本会发光的书
结局: 当一只会飞的龙在在一个神秘的图书馆里发现了一本会发光的书时，整个图书馆都被魔法光芒照亮了

5. 比较两个故事:
  故事1:
    角色: 一只会说话的猫
    背景: 在一个神秘的图书馆里
    剧情: 一只会说话的猫在在一个神秘的图书馆里发现了一本会发光的书
    结局: 当一只会说话的猫在在一个神秘的图书馆里发现了一本会发光的书时，整个图书馆都被魔法光芒照亮了

  故事2:
    角色: 一只会飞的龙
    背景: 在一个神秘的图书馆里
    剧情: 一只会飞的龙在在一个神秘的图书馆里发现了一本会发光的书
    结局: 当一只会飞的龙在在一个神秘的图书馆里发现了一本会发光的书时，整个图书馆都被魔法光芒照亮了

=== 演示完成 ===
"""