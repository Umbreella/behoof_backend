from graphene.relay import Node


class FoodNode(Node):
    @classmethod
    def get_node_from_global_id(cls, info, global_id, only_type=None):
        node = super().get_node_from_global_id(info, global_id, only_type)

        if node and node.is_published:
            return node
