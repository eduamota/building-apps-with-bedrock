output "arn" {
    description = "Arn of the knowledgebase"
    value = aws_bedrockagent_knowledge_base.main.arn
}

output "id" {
    description = "ID of the knowledgebase"
    value = aws_bedrockagent_knowledge_base.main.id
}