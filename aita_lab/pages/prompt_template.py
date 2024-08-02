"""The Prompt template Page."""

import reflex as rx

from aita_lab.states.prompt_template import PromptTemplate, PromptTemplateState
from aita_lab.templates import template
from aita_lab.components.codeeditor import code_editor


def prompt_card(pt: PromptTemplate):
    """Create a prompt card."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.chakra.card(
                rx.chakra.vstack(
                    rx.foreach(pt.prompt_lines.split("\n"), lambda line: rx.chakra.text(line, padding="2px")),
                    align_items="flex-start",
                ),
                header=rx.chakra.heading(pt.prompt_template_name, size="md"),
                # adjust the size and make it scrollable
                direction="column",
                overflow="auto",
                height="300px",
                width="50%",
                margin_right="20px",
                cursor="pointer",
                _hover={"background_color": rx.color("gray", 2)},
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(pt.prompt_template_name, size="6"),
            rx.chakra.flex(
                rx.chakra.badge(f"k_shot: {pt.k_shot}"),
                justify="start",
                direction="row",
                padding="4px",
            ),
            rx.chakra.vstack(
                rx.foreach(pt.prompt_lines.split("\n"), lambda line: rx.text(line)),
                align_items="flex-start",
                font_size="sm",
                margin_top="10px",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Close", size="2"),
                ),
                justify="end",
            ),
        ),
    )


def render_question():
    return rx.box(
        rx.chakra.text("A list of built-in prompt templates for you to choose from."),
        rx.chakra.badge(
            "Question: " + PromptTemplateState.question,
            margin_top="10px",
            font_size="md",
            padding="2px"
        ),
    )


def render_builtin_prompt_templates() -> rx.Component:
    return rx.flex(
        render_question(),
        rx.box(
            rx.chakra.flex(
                rx.foreach(
                    PromptTemplateState.prompt_templates,
                    lambda pt:
                    rx.cond(
                        pt.prompt_template_type == "builtin",
                        prompt_card(pt),
                    )
                )
            ),
            margin_top="20px",
            width="100%",
        ),
        direction="column",
        width="100%",
    )


def render_custom_prompt_templates() -> rx.Component:
    return rx.flex(
        rx.box(
            rx.chakra.text("A list of custom prompt templates that you have created."),
            margin_top="20px",
        ),
        rx.box(
            rx.chakra.flex(
                rx.foreach(
                    PromptTemplateState.prompt_templates,
                    lambda pt:
                    rx.cond(
                        pt.prompt_template_type == "custom",
                        prompt_card(pt),
                    )
                )
            ),
            margin_top="20px",
            width="100%",
        ),
        direction="column",
        width="100%",
    )


def render_create_prompt_template() -> rx.Component:
    return rx.flex(
        rx.dialog.root(
            rx.dialog.trigger(
                rx.button(
                    "Create Prompt Template",
                    variant="solid",
                    on_click=PromptTemplateState.toggle_create_prompt_template_dialog,
                ),
            ),
            rx.dialog.content(
                rx.dialog.title("Create Prompt Template", size="6"),
                rx.dialog.description(
                    "Create a new prompt template.",
                    size="2",
                ),
                rx.flex(
                    rx.box(
                        rx.heading("Prompt Template Name", size="2"),
                        rx.input(
                            placeholder="Enter a Prompt Template Name",
                            on_blur=PromptTemplateState.set_prompt_template_name,
                        ),
                    ),
                    rx.box(
                        rx.heading("Copy An Existing Prompt Template", size="2"),
                        rx.select.root(
                            rx.select.trigger(
                                placeholder="Select a Prompt Template",
                                width="100%",
                            ),
                            rx.select.content(
                                rx.foreach(
                                    PromptTemplateState.prompt_templates,
                                    lambda pt: rx.select.item(
                                        pt.prompt_template_name,
                                        value=pt.prompt_template_name
                                    )
                                ),
                            ),
                            on_change=lambda x: PromptTemplateState.copy_to_current_prompt_template(x),
                        ),
                        width="100%",
                    ),
                    rx.box(
                        rx.heading("Prompt Representation", size="2"),
                        rx.select(
                            ["SQL", "Pandas"],
                            value=PromptTemplateState.prompt_repr,
                            on_change=PromptTemplateState.set_prompt_repr,
                            placeholder="Select a Prompt Representation",
                            width="100%",
                        ),
                        width="100%",
                    ),
                    rx.box(
                        rx.heading("K-shot", size="2"),
                        rx.input(
                            placeholder="Enter the K-shot value",
                            value=PromptTemplateState.k_shot,
                            on_change=PromptTemplateState.set_k_shot,
                            type="number",
                        ),
                        width="100%",
                    ),
                    rx.box(
                        rx.heading("Template", size="2"),
                        code_editor(
                            value=PromptTemplateState.prompt_template_lines,
                            width="100%",
                            min_height="20em",
                            minHeight="20em",
                            theme="light",
                            on_change=PromptTemplateState.set_prompt_template_lines,
                        ),
                    ),
                    direction="column",
                    spacing="4",
                    padding_y="2em",
                    width="100%",
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button("Create", size="2"),
                        on_click=PromptTemplateState.create_prompt_template,
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Cancel", size="2",
                            variant="soft",
                            color_scheme="gray",
                            on_click=PromptTemplateState.toggle_create_prompt_template_dialog,
                        )
                    ),
                    spacing="3",
                    justify="end",
                ),
                on_escape_key_down=lambda _: PromptTemplateState.toggle_create_prompt_template_dialog(),
                on_interact_outside=lambda _: PromptTemplateState.toggle_create_prompt_template_dialog(),

            ),
            open=PromptTemplateState.create_prompt_template_dialog_open,
        ),
    )


@template(route="/prompt_template", title="Prompt Template", on_load=PromptTemplateState.on_load())
def prompt_template() -> rx.Component:
    """The prompt template page.

    Returns:
        The UI for the prompt template page.
    """
    return rx.vstack(
        rx.heading("Builtin Prompt Templates", size="8"),
        rx.divider(),
        render_builtin_prompt_templates(),
        rx.divider(),
        rx.heading("Custom Prompt Templates", size="8"),
        render_create_prompt_template(),
        render_custom_prompt_templates(),
        width="100%",
    )
