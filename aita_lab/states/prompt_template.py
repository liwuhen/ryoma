from typing import List

import json

import reflex as rx

from aita.prompt.prompt_builder import prompt_factory

f = open("aita/prompt/templates/formatted_data.json")
data = json.load(f)


class PromptTemplate(rx.Model):
    prompt_repr: str
    k_shot: int
    example_format: str
    selector_type: str
    prompt_template_name: str
    prompt_lines: List[str]


class PromptTemplateState(rx.State):
    question: str = data["question"]
    prompt_template_names: List[str] = []
    prompt_templates: List[PromptTemplate] = []

    def load_prompt_templates(self):
        prompt_template_names = []
        prompt_templates = []
        for template in data["templates"]:
            prompt_repr = template["args"]["prompt_repr"]
            k_shot = template["args"]["k_shot"]
            example_format = template["args"]["example_type"]
            selector_type = template["args"]["selector_type"]
            prompt_template_name = (
                f"{prompt_repr}_{k_shot}-SHOT_{selector_type}_{example_format}_template"
            )
            prompt_lines = template["formatted_question"]["prompt"].split("\n")
            prompt_template = PromptTemplate(
                prompt_repr=prompt_repr,
                k_shot=k_shot,
                example_format=example_format,
                selector_type=selector_type,
                prompt_template_name=prompt_template_name,
                prompt_lines=prompt_lines,
            )
            prompt_template_names.append(prompt_template_name)
            prompt_templates.append(prompt_template)
        self.prompt_template_names = prompt_template_names
        self.prompt_templates = prompt_templates

    def get_prompt_template(self, prompt_template_name: str) -> PromptTemplate:
        for prompt_template in self.prompt_templates:
            if prompt_template.prompt_template_name == prompt_template_name:
                return prompt_template
        return None

    @staticmethod
    def build_prompt(prompt_template: PromptTemplate, embedding_model: str, target):
        prompt = prompt_factory(
            repr_type=prompt_template.prompt_repr,
            k_shot=0,
            example_format=prompt_template.example_format,
            selector_type=prompt_template.selector_type,
        )(tokenizer=embedding_model)
        target_prompt = prompt.format(target, 2048, 200, 100, cross_domain=False)
        return target_prompt["prompt"]

    def on_load(self):
        self.load_prompt_templates()