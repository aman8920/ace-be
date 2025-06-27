from functools import partial

from old.models import ModularUPCLocation


def expand_facings(modular_plan: list[ModularUPCLocation]) -> list[ModularUPCLocation]:
    # modular_plan = modular_plan["modular_plan"]

    def sort_fn(scope: str = "modular"):
        @partial
        def inner(x: ModularUPCLocation) -> int:
            return x.model_dump(mode="json")[f"{scope}_loc_id"]

        return inner

    modular_plan = sorted(modular_plan, key=sort_fn(scope="shelf"), reverse=True)

    for modular_upc_location in modular_plan:
        print(modular_upc_location)

    return modular_plan
