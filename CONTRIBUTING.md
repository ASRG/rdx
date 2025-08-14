# Contributing

## How to Contribute
- Propose schema improvements (JSON or XML)
- Add examples and test vectors
- File issues for interoperability problems
- Docs and ISO/SAE 21434 mapping improvements

## Requirements Process
**Important:** All new requirements must be tracked through GitHub Issues:
1. Create a new issue describing the requirement
2. Use the appropriate label (`enhancement`, `bug`, `documentation`)
3. Reference the issue number in your PR
4. Update `REQUIREMENTS.md` with the new requirement and issue reference

## Development Workflow
1. **Fork and create a feature branch**
   - Name your branch descriptively (e.g., `feature/add-relationships`, `fix/validation-error`)
   
2. **Update schema and add/adjust examples**
   - Ensure changes maintain backward compatibility
   - Add corresponding examples for new features
   
3. **Run validation**
   ```bash
   ./tools/validate.sh
   ```
   - Ensure all JSON examples validate against the schema
   - Fix any validation errors before proceeding
   
4. **Open a PR with a clear description**
   - Reference the issue number (e.g., "Fixes #123" or "Implements #456")
   - Provide rationale for changes
   - Include test results from validation

## Automated Review Process
This repository uses GitHub Actions with Claude AI for automated code review:

### On Pull Requests
- Claude automatically reviews all PRs when opened or updated
- Reviews focus on:
  - ISO/SAE 21434 compliance
  - Schema consistency
  - Backward compatibility
  - Data model integrity

### On Issues
- New issues are automatically analyzed by Claude
- Claude will:
  - Categorize the issue type (bug, feature, question)
  - Suggest implementation approaches
  - Ask clarifying questions if needed
  - Recommend appropriate labels

### Triggering Manual Review
- Mention `@claude` in any comment to request assistance
- Works in issues, PRs, and review comments

## Code Standards
- Maintain strict JSON Schema validation
- Follow semantic versioning principles
- Document all breaking changes
- Ensure CycloneDX compatibility
- Add comprehensive examples for new features

## Testing Requirements
Before submitting a PR:
- [ ] All examples validate successfully
- [ ] New features have corresponding examples
- [ ] Schema changes are documented
- [ ] REQUIREMENTS.md is updated if applicable
- [ ] Issue number is referenced in PR

## Getting Help
- Check existing issues for similar problems
- Review the methodology documentation
- Ask questions in issue discussions
- Tag `@claude` for AI assistance
