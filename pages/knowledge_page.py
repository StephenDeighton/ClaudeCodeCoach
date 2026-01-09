"""
Knowledge Page for Claude Code Coach
Browse and search the knowledge base
"""

import flet as ft
from theme import Colors, Spacing, Radius, Typography, section_header, divider
from services.knowledge_service import get_knowledge_service, Topic, SearchResult


class KnowledgePage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.knowledge_service = get_knowledge_service()

        # State
        self.current_topic: Topic = None
        self.search_results: list[SearchResult] = []
        self.selected_category: str = None

        # UI components
        self.search_field = ft.TextField(
            hint_text="Search knowledge base...",
            prefix_icon=ft.Icons.SEARCH_ROUNDED,
            on_submit=self._on_search,
            expand=True,
        )

        self.search_button = ft.ElevatedButton(
            "Search",
            icon=ft.Icons.SEARCH_ROUNDED,
            on_click=self._on_search,
        )

        self.results_list = ft.Column(
            spacing=Spacing.XS,
            scroll=ft.ScrollMode.AUTO,
        )

        self.detail_pane = ft.Container(
            content=self._build_welcome_message(),
            padding=Spacing.XL,
            expand=True,
        )

        self.category_chips = ft.Row(
            spacing=Spacing.SM,
            wrap=True,
        )

        # Load initial data
        self._load_categories()

    def _load_categories(self):
        """Load category chips"""
        categories = self.knowledge_service.get_all_categories()
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        chips = []

        # "All" chip
        chips.append(
            ft.FilterChip(
                label=ft.Text("All Topics"),
                selected=self.selected_category is None,
                on_click=lambda e: self._on_category_select(None),
            )
        )

        # Category chips
        for cat in categories:
            chips.append(
                ft.FilterChip(
                    label=ft.Text(f"{cat.name} ({cat.topic_count})"),
                    selected=self.selected_category == cat.slug,
                    on_click=lambda e, slug=cat.slug: self._on_category_select(slug),
                )
            )

        self.category_chips.controls = chips
        self.page.update()

    def _on_category_select(self, category_slug: str):
        """Handle category selection"""
        self.selected_category = category_slug
        self.search_field.value = ""

        if category_slug:
            # Show topics in category
            topics = self.knowledge_service.get_topics_by_category(category_slug)
            self._display_topic_list(topics)
        else:
            # Show all recent topics
            topics = self.knowledge_service.get_recent_topics(limit=20)
            self._display_topic_list(topics)

        self._load_categories()  # Update chip selection
        self.page.update()

    def _on_search(self, e):
        """Handle search submission"""
        query = self.search_field.value.strip()

        if not query:
            self._on_category_select(self.selected_category)
            return

        # Perform search
        self.search_results = self.knowledge_service.search(query, limit=20)

        if self.search_results:
            self._display_search_results()
        else:
            self._display_no_results()

        self.page.update()

    def _display_search_results(self):
        """Display search results in left pane"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        results = []
        for result in self.search_results:
            topic = result.topic

            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            topic.title,
                            size=Typography.BODY_MD,
                            weight=ft.FontWeight.BOLD,
                            color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                        ),
                        ft.Text(
                            result.snippet,
                            size=Typography.BODY_SM,
                            color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text(
                                        topic.category.replace("-", " ").title(),
                                        size=Typography.TINY,
                                        color=Colors.ACCENT_500,
                                    ),
                                    padding=ft.padding.symmetric(horizontal=Spacing.SM, vertical=2),
                                    bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_500),
                                    border_radius=Radius.SM,
                                ),
                                ft.Text(
                                    f"• {topic.difficulty}",
                                    size=Typography.TINY,
                                    color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                                ),
                            ],
                            spacing=Spacing.SM,
                        ),
                    ],
                    spacing=Spacing.XS,
                ),
                padding=Spacing.MD,
                border=ft.border.all(1, Colors.LIGHT_BORDER if not is_dark else Colors.PRIMARY_600),
                border_radius=Radius.MD,
                ink=True,
                on_click=lambda e, t=topic: self._on_topic_select(t),
            )

            results.append(card)

        self.results_list.controls = results

    def _display_topic_list(self, topics: list[Topic]):
        """Display topic list in left pane"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        if not topics:
            self.results_list.controls = [
                ft.Container(
                    content=ft.Text(
                        "No topics found in this category",
                        size=Typography.BODY_SM,
                        color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                        italic=True,
                    ),
                    padding=Spacing.MD,
                )
            ]
            return

        cards = []
        for topic in topics:
            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            topic.title,
                            size=Typography.BODY_MD,
                            weight=ft.FontWeight.BOLD,
                            color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                        ),
                        ft.Text(
                            topic.summary,
                            size=Typography.BODY_SM,
                            color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                    ],
                    spacing=Spacing.XS,
                ),
                padding=Spacing.MD,
                border=ft.border.all(1, Colors.LIGHT_BORDER if not is_dark else Colors.PRIMARY_600),
                border_radius=Radius.MD,
                ink=True,
                on_click=lambda e, t=topic: self._on_topic_select(t),
            )
            cards.append(card)

        self.results_list.controls = cards

    def _display_no_results(self):
        """Display no results message"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        self.results_list.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.SEARCH_OFF_ROUNDED,
                            size=48,
                            color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                        ),
                        ft.Text(
                            "No results found",
                            size=Typography.BODY_MD,
                            weight=ft.FontWeight.BOLD,
                            color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                        ),
                        ft.Text(
                            "Try different keywords or browse by category",
                            size=Typography.BODY_SM,
                            color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=Spacing.SM,
                ),
                padding=Spacing.XL,
            )
        ]

    def _on_topic_select(self, topic: Topic):
        """Handle topic selection - display in detail pane"""
        self.current_topic = topic
        self.detail_pane.content = self._build_topic_detail()
        self.page.update()

    def select_topic_by_slug(self, topic_slug: str):
        """Public method to select and display a topic by slug (for external navigation)."""
        topic = self.knowledge_service.get_topic_by_slug(topic_slug)
        if topic:
            self._on_topic_select(topic)

    def _build_welcome_message(self) -> ft.Control:
        """Build welcome message for empty detail pane"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        return ft.Column(
            [
                ft.Icon(
                    ft.Icons.MENU_BOOK_ROUNDED,
                    size=64,
                    color=Colors.ACCENT_500,
                ),
                ft.Text(
                    "Knowledge Base",
                    size=Typography.H1,
                    weight=ft.FontWeight.BOLD,
                    color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                ),
                ft.Text(
                    "Search for topics or browse by category",
                    size=Typography.BODY_MD,
                    color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=Spacing.MD,
        )

    def _build_topic_detail(self) -> ft.Control:
        """Build detailed topic view"""
        if not self.current_topic:
            return self._build_welcome_message()

        is_dark = self.page.theme_mode == ft.ThemeMode.DARK
        topic = self.current_topic

        # Commands section
        commands_section = None
        if topic.commands:
            commands_section = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "⌨️ Commands & Shortcuts",
                            size=Typography.BODY_SM,
                            weight=ft.FontWeight.BOLD,
                            color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text(
                                        cmd,
                                        size=Typography.BODY_SM,
                                        color=Colors.ACCENT_500,
                                    ),
                                    padding=ft.padding.symmetric(horizontal=Spacing.SM, vertical=4),
                                    bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_500),
                                    border_radius=Radius.SM,
                                    border=ft.border.all(1, Colors.ACCENT_500),
                                )
                                for cmd in topic.commands
                            ],
                            spacing=Spacing.SM,
                            wrap=True,
                        ),
                    ],
                    spacing=Spacing.XS,
                ),
                padding=Spacing.MD,
                bgcolor=ft.Colors.with_opacity(0.03, Colors.ACCENT_500),
                border_radius=Radius.MD,
            )

        # Related topics section
        related_section = None
        if topic.related_topics:
            related_topics = self.knowledge_service.get_related_topics(topic.slug)
            if related_topics:
                related_section = ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "🔗 Related Topics",
                                size=Typography.BODY_SM,
                                weight=ft.FontWeight.BOLD,
                                color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                            ),
                            ft.Column(
                                [
                                    ft.TextButton(
                                        content=ft.Row(
                                            [
                                                ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=16),
                                                ft.Text(rt.title, size=Typography.BODY_SM),
                                            ],
                                            spacing=Spacing.XS,
                                        ),
                                        on_click=lambda e, t=rt: self._on_topic_select(t),
                                    )
                                    for rt in related_topics
                                ],
                                spacing=0,
                            ),
                        ],
                        spacing=Spacing.XS,
                    ),
                    padding=Spacing.MD,
                    border=ft.border.all(1, Colors.LIGHT_BORDER if not is_dark else Colors.PRIMARY_600),
                    border_radius=Radius.MD,
                )

        # Build full detail view
        return ft.Column(
            [
                # Header with category and difficulty
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(
                                topic.category.replace("-", " ").title(),
                                size=Typography.CAPTION,
                                color=Colors.ACCENT_500,
                                weight=ft.FontWeight.BOLD,
                            ),
                            padding=ft.padding.symmetric(horizontal=Spacing.SM, vertical=4),
                            bgcolor=ft.Colors.with_opacity(0.1, Colors.ACCENT_500),
                            border_radius=Radius.SM,
                        ),
                        ft.Container(
                            content=ft.Text(
                                topic.difficulty.upper(),
                                size=Typography.CAPTION,
                                color=Colors.TEXT_DARK_MUTED if not is_dark else Colors.TEXT_LIGHT_MUTED,
                            ),
                            padding=ft.padding.symmetric(horizontal=Spacing.SM, vertical=4),
                            border=ft.border.all(1, Colors.LIGHT_BORDER if not is_dark else Colors.PRIMARY_600),
                            border_radius=Radius.SM,
                        ),
                    ],
                    spacing=Spacing.SM,
                ),
                ft.Container(height=Spacing.SM),
                # Title
                ft.Text(
                    topic.title,
                    size=Typography.H1,
                    weight=ft.FontWeight.BOLD,
                    color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                    selectable=True,
                ),
                ft.Container(height=Spacing.SM),
                # Summary
                ft.Container(
                    content=ft.Text(
                        topic.summary,
                        size=Typography.BODY_LG,
                        color=Colors.TEXT_DARK if not is_dark else Colors.TEXT_LIGHT,
                        selectable=True,
                    ),
                    padding=Spacing.MD,
                    bgcolor=ft.Colors.with_opacity(0.03, Colors.ACCENT_500),
                    border_radius=Radius.MD,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, Colors.ACCENT_500)),
                ),
                ft.Container(height=Spacing.MD),
                # Commands section
                *([ commands_section, ft.Container(height=Spacing.MD)] if commands_section else []),
                # Copy button
                ft.ElevatedButton(
                    "Copy Content to Clipboard",
                    icon=ft.Icons.CONTENT_COPY_ROUNDED,
                    on_click=lambda e: self._copy_to_clipboard(),
                ),
                ft.Container(height=Spacing.MD),
                ft.Divider(),
                # Content (markdown)
                ft.Markdown(
                    topic.content,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    on_tap_link=lambda e: self.page.launch_url(e.data),
                ),
                ft.Container(height=Spacing.MD),
                # Related topics section
                *([ ft.Divider(), related_section] if related_section else []),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )

    def _copy_to_clipboard(self):
        """Copy current topic content to clipboard"""
        if not self.current_topic:
            return

        # Format for clipboard
        content = f"""# {self.current_topic.title}

{self.current_topic.summary}

---

{self.current_topic.content}
"""

        self.page.set_clipboard(content)
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Content copied to clipboard!"),
            bgcolor=Colors.GREEN_500,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def build(self) -> ft.Control:
        """Build knowledge page"""
        is_dark = self.page.theme_mode == ft.ThemeMode.DARK

        # Search section
        search_section = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [self.search_field, self.search_button],
                        spacing=Spacing.SM,
                    ),
                    ft.Container(height=Spacing.SM),
                    self.category_chips,
                ],
                spacing=Spacing.XS,
            ),
            padding=Spacing.MD,
        )

        # Results list (left pane)
        left_pane = ft.Container(
            content=self.results_list,
            width=350,
            padding=Spacing.MD,
            bgcolor=ft.Colors.with_opacity(0.02, Colors.PRIMARY_900 if not is_dark else Colors.PRIMARY_100),
        )

        # Main layout
        content = ft.Container(
            content=ft.Column(
                [
                    # Header
                    section_header(
                        "Knowledge Base",
                        "Learn about Claude Code best practices",
                        ft.Icons.MENU_BOOK_ROUNDED,
                        Colors.ACCENT_500,
                        is_dark=is_dark,
                    ),
                    divider(is_dark=is_dark),
                    # Search
                    search_section,
                    ft.Container(height=Spacing.SM),
                    # Two-pane layout
                    ft.Row(
                        [
                            left_pane,
                            ft.VerticalDivider(width=1),
                            self.detail_pane,
                        ],
                        spacing=0,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            expand=True,
        )

        # Show recent topics initially
        topics = self.knowledge_service.get_recent_topics(limit=20)
        self._display_topic_list(topics)

        return content
